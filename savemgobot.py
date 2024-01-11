import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from embeds import lobby_embed
from api_data import get_lobby_Data, get_total_players, run_api_request, get_all_lobby_ids
import json

bot_token = "Your bot token"

def check_guild_data_json():
    try:
        with open("guild_data.json") as json_file_read:
            channel_ids = json.load(json_file_read)
        return channel_ids
    except Exception as e:
        print(e)
        return {}


def check_locale_json():
    try:
        with open("guilds_locale.json") as json_file_read:
            locale = json.load(json_file_read)
        return locale
    except Exception as e:
        print(e)
        return {}


locales = check_locale_json()


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="*", intents=intents)
    channel_ids = check_guild_data_json()

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
                    msg_list = {guild_id: {}}
                    lobby_ids_contained = {guild_id: []}
                    bot.loop.create_task(channel_name_change(guild_id))
                    with open("guilds_locale.json", "r") as json_file_modify:
                        locale_selection = json.load(json_file_modify)
                        json_file_modify.close()
                    locale_selection[guild_id] = "us_locale"
                    with open("guilds_locale.json", "w") as json_file_modify:
                        json.dump(locale_selection, json_file_modify, indent=6)
                        json_file_modify.close()
                    locales = check_locale_json()
                    await lobbies_channel.purge(limit=100)
                    await start_bot_loop_on_ready(lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained,
                                                  guild_id)
            else:
                await interaction.response.send_message("You must be an administrator to use this command.")
        except Exception as e:
            print(e)

    @bot.tree.command(name="add_host")
    @app_commands.describe(host_name="Input host character name for when a lobby is locked.",
                           discord_contact="Input how to contact this host"
                           )
    async def add_host(interaction: discord.Interaction, host_name: str, discord_contact: str):
        if (interaction.guild_id == 809840002989162516 or
                interaction.guild_id == 833996481144291348 or
                interaction.guild_id == 1175801060888162344):
            user_role_ids = [role.id for role in interaction.user.roles]
            if (
                    interaction.user.guild_permissions.administrator or 809858802278989884 in user_role_ids or 810647505896210482 in user_role_ids):
                with open("hosts.json", "r") as f:
                    hosts = json.load(f)
                hosts[host_name] = discord_contact
                with open("hosts.json", "w") as f:
                    json.dump(hosts, f, indent=6)
                await interaction.response.send_message(f"Host information for {host_name} has been added")
            else:
                await interaction.response.send_message(f"You do not have the necessary role to use this command")
        else:
            await interaction.response.send_message(f"You do not have the permissions to use this command")

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
                locales = check_locale_json()
                await interaction.response.send_message(f"Selected {languages.name} locale.")
            else:
                await interaction.response.send_message("You must be an administrator to use this command.")
        except Exception as e:
            print(e)

    @bot.command(name='sync', description='Owner only')
    async def sync(ctx):
        try:
            if ctx.author.id == 699603124226228275:
                await bot.tree.sync()
            else:
                await ctx.send('You must be the owner of the bot to use this command!')
        except Exception as e:
            print(e)

    @bot.event
    async def on_ready():
        try:
            channel_ids = check_guild_data_json()
            on_ready_loop1 = [on_ready_start(guild_id) for guild_id, channel_id in channel_ids.items()]
            on_ready_loop2 = [channel_name_change(guild_id) for guild_id, channel_id in channel_ids.items()]
            await asyncio.gather(*on_ready_loop1, *on_ready_loop2)
        except Exception as e:
            print(e)

    @bot.event
    async def on_guild_join(guild):
        try:
            await bot.tree.sync(guild=guild)
        except Exception as e:
            print(e)

    async def on_ready_start(guild_id):
        try:
            lobbies_channel = bot.get_channel(channel_ids[guild_id])
            lobby_data_held = {guild_id: []}
            msg_list = {guild_id: {}}
            lobby_ids_contained = {guild_id: []}
            await lobbies_channel.purge(limit=100)
            await start_bot_loop_on_ready(lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained, guild_id)
        except Exception as e:
            print(e)

    async def start_bot_loop_on_ready(lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained, guild_id):
        try:
            global locales
            embed_list = {}
            while True:
                run_api_request()
                all_lobby_data = {guild_id: get_lobby_Data()}
                embed_list[guild_id] = lobby_embed(all_lobby_data[guild_id], locale=locales[guild_id])
                if lobby_data_held[guild_id] != all_lobby_data[guild_id]:
                    await update_lobby_messages(guild_id, embed_list, msg_list, lobbies_channel)
                    lobby_data_held[guild_id] = all_lobby_data[guild_id]
                    lobby_ids_contained[guild_id] = get_all_lobby_ids()
                    print(f"Updated lobby_ids_contained: {lobby_ids_contained[guild_id]}")
                else:
                    print("Lobby list matches")
                await asyncio.sleep(60)
        except Exception as e:
            print(f"Error in start_bot_loop_on_ready for guild_id {guild_id}: {e}")
            print(
                f"lobbies_channel{lobbies_channel}, lobby_data_held{lobby_data_held}, msg_list{msg_list}, lobby_ids_contained{lobby_ids_contained}, guild_id{guild_id}")

    async def channel_name_change(guild_id):
        try:
            while True:
                run_api_request()
                total_players = get_total_players()
                lobbies_channel = bot.get_channel(int(channel_ids[guild_id]))
                await lobbies_channel.edit(name=f"🌐mgo2-lobbies【{total_players}】")
                await asyncio.sleep(601)
        except Exception as e:
            print(f"Error in channel_name_change for guild_id {guild_id}: {e}")

    async def update_lobby_messages(guild_id, embed_list, msg_list, lobbies_channel):
        try:
            api_ids = get_all_lobby_ids()
            for game_id in list(msg_list[guild_id]):
                if game_id not in api_ids:
                    await msg_list[guild_id][game_id].delete()
                    del msg_list[guild_id][game_id]
            for game_id, embed in embed_list[guild_id].items():
                if game_id in msg_list[guild_id]:
                    await msg_list[guild_id][game_id].edit(embed=embed)
                else:
                    msg = await lobbies_channel.send(embed=embed)
                    msg_list[guild_id][game_id] = msg
        except Exception as e:
            print(e)

    bot.run(bot_token)


if __name__ == "__main__":
    run()
