import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from embeds import lobby_embed
from api_data import get_lobby_Data, get_total_players, run_api_request, get_all_lobby_ids
import json
import logging

# Initialize logging
logging.basicConfig(filename='logger.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

bot_token = "bot_token"

def check_json():
    try:
        with open("guild_data.json") as json_file_read:
            channel_ids = json.load(json_file_read)
        return channel_ids
    except Exception as e:
        logging.error(f"Error in check_json: {e}")
        return {}

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    channel_ids = check_json()

    @bot.tree.command(name="set_channel_id")
    @app_commands.describe(userinput="Input the channel ID for the bot.")
    async def channel_id_change(interaction: discord.Interaction, userinput: str):
        try:
            if interaction.user.guild_permissions.administrator:
                guild_id = str(interaction.guild_id)
                channel_ids[guild_id] = int(userinput)
                with open("guild_data.json") as json_file_read:
                    guild_channel_dic = json.load(json_file_read)
                logging.info(f"Channel IDs: {channel_ids[guild_id]} | Guild Channel Dictionary: {guild_channel_dic}")
                channel_id_set = False
                for guild_ids, channel_id in guild_channel_dic.items():
                    if channel_ids[guild_id] == channel_id:
                        channel_id_set = True
                if channel_id_set:
                    await interaction.response.send_message(f"This channel is already stored on our database: {channel_ids[guild_id]}.")
                else:
                    bot.loop.create_task(channel_name_change(guild_id))
                    with open("guild_data.json", "w") as json_file_write:
                        json.dump(channel_ids, json_file_write, indent=6)
                    await interaction.response.send_message(f"Channel ID set to {channel_ids[guild_id]}\nLobbies Generating Enjoy!")
                    logging.info(f"Initial channel_ids: {channel_ids}")
                    lobbies_channel = bot.get_channel(channel_ids[guild_id])
                    lobby_data_held = {guild_id: []}
                    msg_list = {guild_id: {}}
                    lobby_ids_contained = {guild_id: []}
                    bot.loop.create_task(channel_name_change(guild_id))
                    await lobbies_channel.purge(limit=100)
                    await start_bot_loop_on_ready(lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained, guild_id)
            else:
                await interaction.response.send_message("You must be an administrator to use this command.")
        except Exception as e:
            logging.error(f"Error in channel_id_change: {e}")

    @bot.command(name='sync', description='Owner only')
    async def sync(ctx):
        try:
            if ctx.author.id == 699603124226228275:
                await bot.tree.sync()
                logging.info('Command tree synced.')
            else:
                await ctx.send('You must be the owner of the bot to use this command!')
        except Exception as e:
            logging.error(f"Error in sync command: {e}")

    @bot.event
    async def on_ready():
        try:
            logging.info(f'Logged on as {bot.user}!')
            channel_ids = check_json()
            logging.info(f"Channel IDs on ready: {channel_ids}")
            on_ready_loop1 = [on_ready_start(guild_id) for guild_id, channel_id in channel_ids.items()]
            on_ready_loop2 = [channel_name_change(guild_id) for guild_id, channel_id in channel_ids.items()]
            await asyncio.gather(*on_ready_loop1, *on_ready_loop2)
        except Exception as e:
            logging.error(f"Error in on_ready: {e}")

    @bot.event
    async def on_guild_join(guild):
        try:
            await bot.tree.sync(guild=guild)
            logging.info(f"Registered commands in new guild: {guild.name} (ID: {guild.id})")
        except Exception as e:
            logging.error(f"Error in on_guild_join: {e}")

    async def on_ready_start(guild_id):
        try:
            lobbies_channel = bot.get_channel(channel_ids[guild_id])
            lobby_data_held = {guild_id: []}
            msg_list = {guild_id: {}}
            lobby_ids_contained = {guild_id: []}
            await lobbies_channel.purge(limit=100)
            await start_bot_loop_on_ready(lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained, guild_id)
        except Exception as e:
            logging.error(f"Error in on_ready_start for guild_id {guild_id}: {e}")

    async def start_bot_loop_on_ready(lobbies_channel, lobby_data_held, msg_list, lobby_ids_contained, guild_id):
        try:
            embed_list = {}
            while True:
                run_api_request()
                all_lobby_data = {guild_id: get_lobby_Data()}
                embed_list[guild_id] = lobby_embed(all_lobby_data[guild_id])
                if lobby_data_held[guild_id] != all_lobby_data[guild_id]:
                    await update_lobby_messages(guild_id, embed_list, msg_list, lobbies_channel)
                    lobby_data_held[guild_id] = all_lobby_data[guild_id]
                    lobby_ids_contained[guild_id] = get_all_lobby_ids()
                    logging.info(f"Updated lobby_ids_contained: {lobby_ids_contained[guild_id]}")
                else:
                    logging.info("Lobby list matches")
                await asyncio.sleep(60)
        except Exception as e:
            logging.error(f"Error in start_bot_loop_on_ready for guild_id {guild_id}: {e}")

    async def channel_name_change(guild_id):
        try:
            while True:
                run_api_request()
                total_players = get_total_players()
                lobbies_channel = bot.get_channel(int(channel_ids[guild_id]))
                await lobbies_channel.edit(name=f"🌐mgo2-lobbies【{total_players}】")
                await asyncio.sleep(601)
        except Exception as e:
            logging.error(f"Error in channel_name_change for guild_id {guild_id}: {e}")

    async def update_lobby_messages(guild_id, embed_list, msg_list, lobbies_channel):
        try:
            api_ids = get_all_lobby_ids()
            for game_id in list(msg_list[guild_id]):
                if game_id not in api_ids:
                    logging.info(f"Deleting message for game_id {game_id}")
                    await msg_list[guild_id][game_id].delete()
                    del msg_list[guild_id][game_id]
            for game_id, embed in embed_list[guild_id].items():
                if game_id in msg_list[guild_id]:
                    logging.info(f"Editing message for game_id {game_id}")
                    await msg_list[guild_id][game_id].edit(embed=embed)
                else:
                    logging.info(f"Sending new embed for game_id {game_id}")
                    msg = await lobbies_channel.send(embed=embed)
                    msg_list[guild_id][game_id] = msg
        except Exception as e:
            logging.error(f"Error in update_lobby_messages for guild_id {guild_id}: {e}")

    bot.run(bot_token)

if __name__ == "__main__":
    run()
