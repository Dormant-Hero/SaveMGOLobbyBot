import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from embeds import lobby_embed
from api_data import get_lobby_Data, get_total_players, run_api_request, get_all_lobby_ids
import json

bot_token = "Your bot token"

# Stores guild id's and their respective selected channel id
def check_json():
    json_file_read = open("guild_data.json")
    channel_ids = json.load(json_file_read)
    json_file_read.close()
    return channel_ids

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    # Global dictionary to store channel IDs for each server
    channel_ids = check_json()

    # Application command to setup channel when the bot first joins a Discord Server
    @bot.tree.command(name="set_channel_id")
    @app_commands.describe(userinput="Input the channel ID for the bot.")
    async def channel_id_change(interaction: discord.Interaction, userinput: str):
        if interaction.user.guild_permissions.administrator:
            guild_id = str(interaction.guild_id)
            channel_ids[guild_id] = int(userinput)
            json_file_read = open("guild_data.json")
            if channel_ids[guild_id] in json.load(json_file_read):
                await interaction.response.send_message(
                    f"This channel is already stored on our database {channel_ids[guild_id]}")
                json_file_read.close()
            else:
                await interaction.response.send_message(f"Channel ID set to {channel_ids[guild_id]}")
                bot.loop.create_task(channel_name_change(guild_id))  # Corrected this line
                json_file_write = open("guild_data.json", "w")
                json.dump(channel_ids, json_file_write, indent=6)
                json_file_write.close()
        else:
            await interaction.response.send_message("You must be an administrator to use this command.")

    # This is to sync all the bots / applications to all servers once I have created new ones. Takes a while to sync
    @bot.command(name='sync', description='Owner only')
    async def sync(ctx):
        if ctx.author.id == 699603124226228275:
            await bot.tree.sync()
            print('Command tree synced.')
        else:
            await ctx.response.send_message('You must be the owner of th ebot to use this command!')

    # Used to start the bot the very first time it is brought to your server. Likely to remove this in the future and have set channel do this bit.
    @bot.command()
    async def start(ctx):
        print(f"Initial channel_ids: {channel_ids}")
        guild_id = str(ctx.guild.id)
        if guild_id in channel_ids and ctx.channel.id == channel_ids[guild_id]:
            print("Code has started")
            lobbies_channel = bot.get_channel(channel_ids[guild_id])
            lobby_data_held = {guild_id: []}
            msg_list = {guild_id: {}}
            lobby_ids_contained = {guild_id: []}
            bot.loop.create_task(channel_name_change(guild_id))
            await lobbies_channel.purge(limit=100)
            await start_bot_loop(ctx, lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained)
        else:
            await ctx.send(f"This command can only be used in the assigned channel for this server.")

    # on activation lets me know that the bot is logged on/connected runs numerous instances of a for loop
    @bot.event
    async def on_ready():
        print(f'Logged on as {bot.user}!')
        check_json()
        channel_ids = check_json()
        print(channel_ids)
        on_ready_loop1 = [on_ready_start(guild_id) for guild_id, channel_id in channel_ids.items()]
        on_ready_loop2 = [channel_name_change(guild_id) for guild_id, channel_id in channel_ids.items()]
        await asyncio.gather(*on_ready_loop1, *on_ready_loop2)

    # should sync the bots applications on guild join
    @bot.event
    async def on_guild_join(guild):
        await bot.tree.sync(guild=guild)
        print(f"Registered commands in new guild: {guild.name} (ID: {guild.id})")

    # How my bot starts when on ready and already setup before.
    async def on_ready_start(guild_id):
        lobbies_channel = bot.get_channel(channel_ids[guild_id])
        lobby_data_held = {guild_id: []}
        msg_list = {guild_id: {}}
        lobby_ids_contained = {guild_id: []}
        await lobbies_channel.purge(limit=100)
        await start_bot_loop_on_ready(lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained, guild_id)

    # The bot loop when the bot starts
    async def start_bot_loop_on_ready(lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained, guild_id):
        embed_list = {}
        while True:
            run_api_request()
            all_lobby_data = {guild_id: get_lobby_Data()}
            embed_list[guild_id] = lobby_embed(all_lobby_data[guild_id])
            if lobby_data_held[guild_id] != all_lobby_data[guild_id]:
                await update_lobby_messages(guild_id, embed_list, msg_list, lobbies_channel)
                lobby_data_held[guild_id] = all_lobby_data[guild_id]
                lobby_ids_contained[guild_id] = get_all_lobby_ids()
                print(f"Updated lobby_ids_contained: {lobby_ids_contained[guild_id]}")
            else:
                print("Lobby list matches")
            await asyncio.sleep(60)


    # channel name changer function (gets activated once channel is set by discord admin)
    async def channel_name_change(guild_id):
        while True:
            run_api_request()
            total_players = get_total_players()
            lobbies_channel = bot.get_channel(int(channel_ids[guild_id]))
            await lobbies_channel.edit(name=f"🌐mgo2-lobbies【{total_players}】")
            await asyncio.sleep(601)  # Discord rate limits channel name changing so had to set 10 mins


    #checks api in msg list against api and deletes any that no longer exist
    async def update_lobby_messages(guild_id, embed_list, msg_list, lobbies_channel):
        api_ids = get_all_lobby_ids()
        for game_id in list(msg_list[guild_id]):
            if game_id not in api_ids:
                print(f"Deleting message for game_id {game_id}")
                await msg_list[guild_id][game_id].delete()
                del msg_list[guild_id][game_id]

        #provides new embed data for existing lobbies and posts for those that do not exist already as a message
        for game_id, embed in embed_list[guild_id].items():
            if game_id in msg_list[guild_id]:
                print(f"Editing message for game_id {game_id}")
                await msg_list[guild_id][game_id].edit(embed=embed)
            else:
                print(f"Sending new embed for game_id {game_id}")
                msg = await lobbies_channel.send(embed=embed)
                msg_list[guild_id][game_id] = msg

    # the bot loop function when you do !start for the very first time you setup my bot
    async def start_bot_loop(ctx, lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained):
        guild_id = str(ctx.guild.id)
        embed_list = {}
        while True:
            run_api_request()
            all_lobby_data = {guild_id: get_lobby_Data()}
            embed_list[guild_id] = lobby_embed(all_lobby_data[guild_id])
            if lobby_data_held[guild_id] != all_lobby_data[guild_id]:
                await update_lobby_messages(guild_id, embed_list, msg_list, lobbies_channel)
                lobby_data_held[guild_id] = all_lobby_data[guild_id]
                lobby_ids_contained[guild_id] = get_all_lobby_ids()
                print(f"Updated lobby_ids_contained: {lobby_ids_contained[guild_id]}")
            else:
                print("Lobby list matches")
            await asyncio.sleep(60)

    bot.run(bot_token)


if __name__ == "__main__":
    run()
