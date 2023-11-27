import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from embeds import lobby_embed
from api_data import get_lobby_Data, get_total_players, run_api_request, get_all_lobby_ids

bot_token = "Your Bot token"
channel_id = 0 # channel id number goes here

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    # Global dictionary to store channel IDs for each server
    channel_ids = {}

    # on activation lets me know that the bot is logged on/connected
    @bot.event
    async def on_ready():
        print(f'Logged on as {bot.user}!')

    @bot.tree.command(name="set_channel_id")
    @app_commands.describe(userinput="Input the channel ID for the bot.")
    async def channel_id_change(interaction: discord.Interaction, userinput: str):
        if interaction.user.guild_permissions.administrator:
            guild_id = interaction.guild_id
            channel_ids[guild_id] = int(userinput)
            await interaction.response.send_message(f"Channel ID set to {channel_ids[guild_id]}")
            bot.loop.create_task(channel_name_change(guild_id))  # Corrected this line
        else:
            await interaction.response.send_message("You must be an administrator to use this command.")

    # channel name changer function (gets activated once channel is set by discord admin)
    async def channel_name_change(guild_id):
        while True:
            run_api_request()
            total_players = get_total_players()
            lobbies_channel = bot.get_channel(channel_ids[guild_id])
            await lobbies_channel.edit(name=f"🌐mgo2-lobbies【{total_players}】")
            await asyncio.sleep(601)  # Discord rate limits channel name changing so had to set 10 mins

    # This is to sync all the bots applications to all servers once I have created new ones
    @bot.command(name='sync', description='Owner only')
    async def sync(ctx):
        if ctx.author.id == 699603124226228275:
            await bot.tree.sync()
            print('Command tree synced.')
        else:
            await ctx.response.send_message('You must be the owner of th ebot to use this command!')

    # should sync the bots applications on guild join
    @bot.event
    async def on_guild_join(guild):
        await bot.tree.sync(guild=guild)
        print(f"Registered commands in new guild: {guild.name} (ID: {guild.id})")

    @bot.command()
    async def start(ctx):
        """Shows lobbies available in mgo2_lobbies channel"""
        guild_id = ctx.guild.id  # Get the server ID
        if guild_id in channel_ids and ctx.channel.id == channel_ids[guild_id]:
            print("Code has started")
            lobbies_channel = bot.get_channel(channel_ids[guild_id])
            lobby_data_held = {guild_id: []}
            msg_list = {guild_id: []}
            lobby_ids_contained = {guild_id: []}
            bot.loop.create_task(channel_name_change(guild_id))
            await lobbies_channel.purge(limit=100)
            while True:
                run_api_request()
                all_lobby_data = {guild_id: get_lobby_Data()}
                embed_list = {guild_id: lobby_embed()}  # embed list simply gets the list from the lobby embed function
                if lobby_data_held[guild_id] == all_lobby_data:
                    print("lobby list matches")
                    await asyncio.sleep(60)
                else:
                    print("embed does not match")
                    if lobby_ids_contained[guild_id] == []:
                        for embed in embed_list[guild_id]:
                            msg = await lobbies_channel.send(embed=embed)
                            msg_list[guild_id].append(msg)
                        lobby_data_held[guild_id] = all_lobby_data
                        lobby_ids_contained[guild_id] = get_all_lobby_ids()
                        await asyncio.sleep(60)
                    elif lobby_ids_contained[guild_id] != []:
                        api_ids = get_all_lobby_ids()

                        # A check if the id is not in the api id. If not in then gets deleted
                        count = 0
                        for id in lobby_ids_contained[guild_id]:
                            if id not in api_ids:
                                await msg_list[guild_id][count].delete()
                                del msg_list[guild_id][count]
                                del lobby_ids_contained[guild_id][count]
                            count += 1

                        # A check if the id is still in the api_ids. If so the message just needs editing
                        count = 0
                        for id in lobby_ids_contained[guild_id]:
                            if id in api_ids:
                                await msg_list[guild_id][count].edit(embed=embed_list[guild_id][count])
                                await asyncio.sleep(2)
                            count += 1

                        # A check if the api has an id not already contained
                        count = 0
                        for id in api_ids:
                            if id not in lobby_ids_contained[guild_id]:
                                msg = await lobbies_channel.send(embed=embed_list[guild_id][count])
                                msg_list[guild_id].append(msg)
                            count += 1
                        lobby_data_held[guild_id] = all_lobby_data
                        lobby_ids_contained[guild_id] = get_all_lobby_ids()
                        await asyncio.sleep(60)
        else:
            await ctx.send(f"This command can only be used in the assigned channel for this server.")

    bot.run(bot_token)


if __name__ == "__main__":
    run()