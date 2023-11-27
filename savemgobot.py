import discord
import asyncio
from discord.ext import commands
from embeds import lobby_embed
from api_data import get_lobby_Data, get_total_players, run_api_request, get_all_lobby_ids

bot_token = "input bopt token here"
guild_name = "Dormant Hero's server"
channel_id = "input channel id"

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
        msg_list = []
        lobby_ids_contained = []
        await lobbies_channel.purge(limit=100)
        while True:
            run_api_request()
            all_lobby_data = get_lobby_Data()
            embed_list = lobby_embed()  # embed list simply gets the list from the lobby embed function
            if lobby_data_held == all_lobby_data:
                print("lobby list matches")
                await asyncio.sleep(60)
            else:
                print("embed does not match")
                if lobby_ids_contained == []:
                    for embed in embed_list:
                        msg = await lobbies_channel.send(embed=embed)
                        msg_list.append(msg)
                    lobby_data_held = all_lobby_data
                    lobby_ids_contained = get_all_lobby_ids()
                    await asyncio.sleep(60)
                elif lobby_ids_contained != []:
                    api_ids = get_all_lobby_ids()

                    # A check if the id is not in the api id. If not in then gets deleted
                    count = 0
                    for id in lobby_ids_contained:
                        if id not in api_ids:
                            await msg_list[count].delete()
                            del msg_list[count]
                            del lobby_ids_contained[count]
                        count += 1

                    # A check if the id is still in the api_ids. If so the message just needs editing
                    count = 0
                    for id in lobby_ids_contained:
                        if id in api_ids:
                            await msg_list[count].edit(embed=embed_list[count])
                            await asyncio.sleep(2)
                        count += 1

                    # A check if the api has an id not already contained
                    count = 0
                    for id in api_ids:
                        if id not in lobby_ids_contained:
                            msg = await lobbies_channel.send(embed=embed_list[count])
                            msg_list.append(msg)
                        count += 1
                    lobby_data_held = all_lobby_data
                    lobby_ids_contained = get_all_lobby_ids()
                    await asyncio.sleep(60)
    bot.run(bot_token)


if __name__ == "__main__":
    run()