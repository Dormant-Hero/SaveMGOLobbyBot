import discord
import asyncio
from discord.ext import commands
from discord import app_commands
import json
from datetime import timedelta
import datetime
import os
from embeds import lobby_embed
from api_data import get_lobby_Data, get_total_players, run_api_request, get_all_lobby_ids
from icecream import ic
import subprocess
import sys
#note the below is pip install python-dotenv to get this one installed!
from dotenv import load_dotenv

load_dotenv()
bot_token = os.environ.get("TOKEN")


def return_chan_id_from_json():
    try:
        with open("guild_data.json") as json_file_read:
            channel_ids = json.load(json_file_read)
        return channel_ids
    except Exception as e:
        ic()
        ic(e)
        return {}


def return_discord_server_locale():
    try:
        with open("guilds_locale.json") as json_file_read:
            locale = json.load(json_file_read)
        return locale
    except Exception as e:
        ic()
        ic(e)
        return {}


locales = return_discord_server_locale()

def restart_bot():
    os.execv(sys.executable, [sys.executable] + sys.argv)


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="*", intents=intents)
    channel_ids = return_chan_id_from_json()

    # Sets the channel id you want the bot to produce MGO2 lobby information in then runs accordingly.
    @bot.tree.command(name="set_channel_id")
    @app_commands.describe(userinput="Input the channel ID for the bot.")
    async def channel_id_change(interaction: discord.Interaction, userinput: str):
        try:
            global locales
            if interaction.user.guild_permissions.administrator:
                guild_id = str(interaction.guild_id)
                channel_ids[guild_id] = int(userinput)
                with open("guild_data.json") as json_file_read:
                    guild_channel_dic = json.load(json_file_read)
                channel_id_set = False
                for guild_ids, channel_id in guild_channel_dic.items():
                    if channel_ids[guild_id] == channel_id:
                        channel_id_set = True
                if channel_id_set:
                    await interaction.response.send_message(
                        f"This channel is already stored on our database: {channel_ids[guild_id]}.")
                else:
                    bot.loop.create_task(channel_name_change(guild_id))
                    with open("guild_data.json", "w") as json_file_write:
                        json.dump(channel_ids, json_file_write, indent=6)
                    await interaction.response.send_message(
                        f"Channel ID set to {channel_ids[guild_id]}\nLobbies Generating Enjoy!")
                    lobbies_channel = bot.get_channel(channel_ids[guild_id])
                    lobby_data_held = {guild_id: []}
                    msg_list = {guild_id: []}
                    lobby_ids_contained = {guild_id: []}
                    bot.loop.create_task(channel_name_change(guild_id))
                    with open("guilds_locale.json", "r") as json_file_modify:
                        locale_selection = json.load(json_file_modify)
                        json_file_modify.close()
                    locale_selection[guild_id] = "us_locale"
                    with open("guilds_locale.json", "w") as json_file_modify:
                        json.dump(locale_selection, json_file_modify, indent=6)
                        json_file_modify.close()
                    locales = return_discord_server_locale()
                    await lobbies_channel.purge(limit=100)
                    await start_bot_loop_on_ready(lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained,
                                                guild_id)
            else:
                await interaction.response.send_message("You must be an administrator to use this command.")
        except Exception as e:
            ic()
            ic(e)

    # Add a hosts contact information for when they host a password locked game
    @bot.tree.command(name="add_host")
    @app_commands.describe(host_name="Input host character name for when a lobby is locked.",
                        discord_contact="Input how to contact this host"
                        )
    async def add_to_hosts_json(interaction: discord.Interaction, host_name: str, discord_contact: str):
        # checks if SaveMGO discord guild as command should only be used there
        if interaction.guild_id == 809840002989162516:
            user_role_ids = [role.id for role in interaction.user.roles]
            if (
                    interaction.user.guild_permissions.administrator or 809858802278989884 in user_role_ids or 810647505896210482 in user_role_ids):
                with open("hosts.json", "r") as locked_host_list:
                    hosts = json.load(locked_host_list)
                hosts[host_name] = discord_contact
                with open("hosts.json", "w") as locked_host_list:
                    json.dump(hosts, locked_host_list, indent=6)
                await interaction.response.send_message(f"Host information for {host_name} has been added")
            else:
                await interaction.response.send_message(f"You do not have the necessary role to use this command")
        else:
            await interaction.response.send_message(f"You do not have the permissions to use this command")

    # stores the Discord servers favoured locale for the bot
    @bot.tree.command(name="select_language")
    @app_commands.describe(languages="Locales to choose from")
    @app_commands.choices(languages=[
        app_commands.Choice(name='JP', value='jp_locale'),
        app_commands.Choice(name='US', value='us_locale'),
    ])
    async def locale_change(interaction: discord.Interaction, languages: app_commands.Choice[str]):
        global locales
        try:
            if interaction.user.guild_permissions.administrator:
                guild_id = str(interaction.guild_id)
                with open("guilds_locale.json", "r") as json_file_modify:
                    locale_selection = json.load(json_file_modify)
                locale_selection[guild_id] = languages.value
                with open("guilds_locale.json", "w") as json_file_modify:
                    json.dump(locale_selection, json_file_modify, indent=6)
                locales = return_discord_server_locale()
                await interaction.response.send_message(f"Selected {languages.name} locale.")
            else:
                await interaction.response.send_message("You must be an administrator to use this command.")
        except Exception as e:
            ic()
            ic(e)

    # syncs the bot commands to Discord's servers. Set to owner only so it is not abused.
    @bot.command(name='sync', description='Owner only')
    async def sync(ctx):
        try:
            if ctx.author.id == 699603124226228275:
                await bot.tree.sync()
            else:
                await ctx.send('You must be the owner of the bot to use this command!')
        except Exception as e:
            ic()
            ic(e)

    # on ready functionality. Bot will produce lobby info and change channel names
    @bot.event
    async def on_ready():
        try:
            channel_ids = return_chan_id_from_json()
            on_ready_loop1 = [on_ready_start(guild_id) for guild_id, channel_id in channel_ids.items()]
            on_ready_loop2 = [channel_name_change(guild_id) for guild_id, channel_id in channel_ids.items()]
            await asyncio.gather(*on_ready_loop1, *on_ready_loop2)
        except Exception as e:
            ic()
            ic(e)

    # bot attempts to sync commands upon joining any discord guild
    @bot.event
    async def on_guild_join(guild):
        try:
            await bot.tree.sync(guild=guild)
        except Exception as e:
            ic()
            ic(e)

    # when the bot boots purges the channel and runs the function for the MGO games embed messages
    async def on_ready_start(guild_id):
        try:
            lobbies_channel = bot.get_channel(channel_ids[guild_id])
            lobby_data_held = {guild_id: []}
            msg_list = {guild_id: []}
            lobby_ids_contained = {guild_id: []}
            await lobbies_channel.purge(limit=100)
            await start_bot_loop_on_ready(lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained, guild_id)
        except Exception as e:
            ic()
            ic(e)

    # Most of the mgo2 game embed code here
    async def start_bot_loop_on_ready(lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained, guild_id):
        try:
            global locales
            embed_list = {}
            lobby_id_size_sorted = {}
            count = 0
            kimi_event = ""
            while True:
                now = datetime.datetime.now()
                if int(now.minute) == 50:
                    print(f"minute now {now.minute} and second is {now.second}")
                    await asyncio.sleep(60)
                    restart_bot()
                run_api_request()
                all_lobby_data = {guild_id: get_lobby_Data()}
                lobby_embed_func_date = lobby_embed(all_lobby_data[guild_id], locale=locales[guild_id])
                embed_list[guild_id] = lobby_embed_func_date[0]
                kimi_hosting = lobby_embed_func_date[1]
                lobby_id_size_sorted[guild_id] = lobby_embed_func_date[2]
                if lobby_data_held[guild_id] != all_lobby_data[guild_id]:
                    await update_lobby_messages(guild_id, embed_list, msg_list, lobbies_channel, lobby_id_size_sorted,
                                                lobby_ids_contained)
                    lobby_data_held[guild_id] = all_lobby_data[guild_id]
                    lobby_ids_contained[guild_id] = get_all_lobby_ids()
                else:
                    print("Lobby list matches")

                print(f"The guild id is {guild_id} and kimi hosting is {kimi_hosting} and count is {count}")
                if str(guild_id) == "809840002989162516" and kimi_hosting and count == 0:
                    print(guild_id, kimi_hosting, count)
                    guild = bot.get_guild(809840002989162516)
                    kimi_event = await guild.create_scheduled_event(name="MGOPC Academy Session",
                                                                    description="A lobby hosted for new and returning players to learn, relax, practice and ask questions about MGO2.",
                                                                    start_time=discord.utils.utcnow() + timedelta(
                                                                        minutes=5),
                                                                    end_time=discord.utils.utcnow().replace(
                                                                        day=discord.utils.utcnow().day + 1),
                                                                    entity_type=discord.EntityType.external,
                                                                    location="MGOPC Academy",
                                                                    privacy_level=discord.PrivacyLevel.guild_only
                                                                    )
                    count += 1
                elif count == 1 and not kimi_hosting:
                    await kimi_event.delete(reason="Kimidaki is no longer hosting")
                    count = 0
                await asyncio.sleep(60)
        except Exception as e:
            ic()
            ic(f"Line 238Error in start_bot_loop_on_ready for guild_id {guild_id}: {e}")
            ic(
                f"lobbies_channel{lobbies_channel}, lobby_data_held{lobby_data_held}, msg_list{msg_list}, lobby_ids_contained{lobby_ids_contained}, guild_id{guild_id}")
            if lobby_embed_func_date[1]:
                await kimi_event.delete(reason="Kimidaki is no longer hosting")
            start_bot_loop_on_ready(lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained, guild_id)

    # Pulls MGO2 playercount data and changes channel name accordingly every 10 minutes
    async def channel_name_change(guild_id):
        try:
            while True:
                run_api_request()
                total_players = get_total_players()
                lobbies_channel = bot.get_channel(int(channel_ids[guild_id]))
                await lobbies_channel.edit(name=f"🌐mgo2-lobbies【{total_players}】")
                await asyncio.sleep(601)
        except Exception as e:
            print(f"Line 255 Error in channel_name_change for guild_id {guild_id}: {e}")

    # Handles the embed posting/updating process
    async def update_lobby_messages(guild_id, embed_list, msg_list, lobbies_channel, lobby_id_size_sorted,
                                    lobby_ids_contained):
        try:
            count = 0
            while len(msg_list[guild_id]) > len(lobby_id_size_sorted[guild_id]):
                await msg_list[guild_id][-1].delete()
                del msg_list[guild_id][-1]
            for game_id in list(lobby_id_size_sorted[guild_id]):
                if game_id in list(lobby_ids_contained[guild_id]):
                    await msg_list[guild_id][count].edit(embed=embed_list[guild_id][game_id])
                    count += 1
                else:
                    msg = await lobbies_channel.send(embed=embed_list[guild_id][game_id])
                    msg_list[guild_id].append(msg)
        except Exception as e:
            ic()
            ic(e)

    bot.run(bot_token)




if __name__ == "__main__":
    run()
