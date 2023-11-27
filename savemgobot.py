import discord
import asyncio
from discord.ext import commands
from embeds import lobby_embed
from api_data import get_lobby_Data, get_total_players, run_api_request


bot_token = "bot token"
guild_name = "SaveMGO"
channel_id = "channel_id. Must be integer not string when replaced"

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        lobbies_channel = bot.get_channel(channel_id)
        print(f'Logged on as {bot.user}!')
        while True:
            run_api_request()
            total_players = get_total_players()
            await lobbies_channel.edit(name=f"🌐mgo2-lobbies【{total_players}】")
            await asyncio.sleep(601) # Discord rate limits channel name changing and advises it to be done every 10 mins.

    @bot.command()
    async def start(ctx):
        """Shows lobbies available in mgo2_lobbies channel"""
        print("Code has started")
        lobbies_channel = bot.get_channel(channel_id)
        lobby_data_held = []
        while True:
            embed_list = []
            run_api_request()
            all_lobby_data = get_lobby_Data()
            embed_list = lobby_embed()  # embed list simply gets the list from the lobby embed function
            if lobby_data_held == all_lobby_data:
                print("lobby list matches")
                await asyncio.sleep(60)
            else:
                print("embed does not match")
                lobby_data_held = all_lobby_data
                await lobbies_channel.purge(limit=100)
                for embed in embed_list:
                    await lobbies_channel.send(embed=embed)
                await asyncio.sleep(60)


    bot.run(bot_token)

if __name__ == "__main__":
    run()

