from data import map_choices, game_modes, ranks
import re
import discord
import logging


def lobby_embed(all_lobby_data):
    id_embeds = {}
    # A for loop that splits
    for lobby in all_lobby_data:
        all_player_data = lobby["players"]  # All player data from this lobby
        lobby_name = lobby["name"]  #
        current_game = lobby["currentGame"]
        map_no = lobby["games"][current_game][1]
        if map_no not in map_choices:
            logging.debug(f"The map no is {map_no}. Had to use 22 as it does not exist")
            map_no = 22
        map_name = map_choices[map_no][0]
        map_thumbnail = map_choices[map_no][1]
        game_mode_no = lobby["games"][current_game][0]
        if game_mode_no not in game_modes:
            logging.debug(f"The game mode no is {game_mode_no}. Had to use 17 as it does not exist")
            game_mode_no = 17
        game_mode = game_modes[game_mode_no]
        players = len(all_player_data)  # Players in the lobby
        lobby_player_limit = lobby["maxPlayers"]
        region = lobby["location"]
        lobby_id = lobby["id"]
        invisible_space = f"<:invisible:1177474192782929970>{' '}"  # Note special invisible characters used for spacing as normal spaces do not work.
        player_info = ""  # Used for game modes without teams to split the teams into 2 so the embed does not take up too much space.
        player_info2 = ""  # Used for game modes without teams to split the teams into 2 so the embed does not take up too much space.
        count = 0  # Used with the for loop below to indicate how many players in a match for game modes without teams.
        spectators = ""
        player_team_negative_1 = ""  # Unknown what this value is but it is in the code just in case.
        red_team = ""
        blue_team = ""
        sneaking_team = ""
        assigning_team_1 = ""
        assigning_team_2 = ""
        for data in all_player_data:
            player_exp = data["exp"]
            if player_exp >= 4075:
                player_level = 22
            elif player_exp >= 3625:
                player_level = 21
            elif player_exp >= 3275:
                player_level = 20
            elif player_exp >= 2975:
                player_level = 19
            elif player_exp >= 2725:
                player_level = 18
            elif player_exp >= 2525:
                player_level = 17
            elif player_exp >= 2350:
                player_level = 16
            elif player_exp >= 2175:
                player_level = 15
            elif player_exp >= 2000:
                player_level = 14
            elif player_exp >= 1850:
                player_level = 13
            elif player_exp >= 1700:
                player_level = 12
            elif player_exp >= 1550:
                player_level = 10
            elif player_exp >= 1250:
                player_level = 9
            elif player_exp >= 1100:
                player_level = 8
            elif player_exp >= 950:
                player_level = 7
            elif player_exp >= 800:
                player_level = 6
            elif player_exp >= 650:
                player_level = 5
            elif player_exp >= 500:
                player_level = 4
            elif player_exp >= 375:
                player_level = 3
            elif player_exp >= 250:
                player_level = 2
            elif player_exp >= 125:
                player_level = 1
            elif player_exp >= 0:
                player_level = 0

            player_name = re.sub("-", "—", data[
                "name"])  # formats the player name to not have a normal dash as this breaks the code
            player_link = f"https://mgo2pc.com/profile/{re.sub(' ', '%20', data['name'])}"  # Accounts for HTML URL encoding required
            rank_no = int(data["rank"])
            if rank_no not in ranks:
                logging.debug(f"The rank no is {rank_no}. Had to use 0 as it does not exist")
                rank_no = 0
            player_rank_emoji = ranks[rank_no]
            team = data["team"]
            if len(player_name) > 10:
                player_name = player_name[:10] + "..."
            count += 1
            # Splits the player listing in half so the embed takes up less room
            # All the other appends below are just adding player information to variables to be used in the embed later
            if count <= lobby_player_limit / 2:
                player_info += f"\n{player_rank_emoji}{' '}{player_level}[{player_name}]({player_link})"
            else:
                player_info2 += f"\n{player_rank_emoji}{' '}{player_level}{' '}[{player_name}]({player_link})"
            if team == -2:
                spectators += f"\n{player_rank_emoji}{' '}{player_level}{' '}[{player_name}]({player_link})"
            elif team == -1:
                player_team_negative_1 += f"\n{player_rank_emoji}{' '}``{player_level}``{' '}[{player_name}]({player_link})"
                logging.debug(f"Player Team Negative 1 is unknown and I did not expect this to ever happen.")
                logging.info(f"Player team -1 happened in {game_mode} for a game named{lobby_name}\n{player_team_negative_1}")
            elif team == 0:
                red_team += f"\n{player_rank_emoji}{' '}{player_level}{' '}[{player_name}]({player_link})"
            elif team == 1:
                blue_team += f"\n{player_rank_emoji}{' '}{player_level}{' '}[{player_name}]({player_link})"
            elif team == 2:
                sneaking_team += f"\n{player_rank_emoji}{' '}{player_level}{' '}[{player_name}]({player_link})"
            elif team == int(-32) and count <= lobby_player_limit / 2:
                assigning_team_1 += f"\n{player_rank_emoji}{' '}{player_level}{' '}[{player_name}]({player_link})"
            else:
                assigning_team_2 += f"\n{player_rank_emoji}{' '}{player_level}{' '}[{player_name}]({player_link})"

        if len(spectators) >= 1024:
            logging.debug(f"The spectators length is over 1024. The length is{len(spectators)}")
            logging.info(f"Spectator player info below {spectators}")
            spectators = ""
            for data in all_player_data:
                player_name = re.sub("-", "—", data[
                    "name"])  # formats the player name to not have a normal dash as this breaks the code
                player_rank_emoji = ranks[data["rank"]]
                spectators += f"\n {player_rank_emoji}{' '}``{player_level}``{' '}[{player_name}]({player_link})"
            if len(spectators) >= 1024:
                logging.debug(f"The spectators length is over 1024 even with links removed. The length is{len(spectators)}")
                logging.info(f"Spectator player info below\n{spectators}")
                spectators = "Investigating this bug"

        if len(red_team) >= 1024:
            logging.debug(f"The red team length is over 1024. The length is{len(red_team)}")
            logging.info(f"Spectator player info below\n{red_team}")
            red_team = ""
            for data in all_player_data:
                player_name = re.sub("-", "—", data[
                    "name"])  # formats the player name to not have a normal dash as this breaks the code
                player_rank_emoji = ranks[data["rank"]]
                red_team += f"\n[ {player_rank_emoji}{' '}{player_name}]"
            if len(red_team) >= 1024:
                logging.debug(f"The red_team length is over 1024 even with links removed. The length is{len(red_team)}")
                logging.info(f"Spectator player info below {red_team}")
                red_team = "Investigating this bug"

        if len(blue_team) >= 1024:
            logging.debug(f"The red team length is over 1024. The length is{len(blue_team)}")
            logging.info(f"Spectator player info below\n{blue_team}")
            blue_team = ""
            for data in all_player_data:
                player_name = re.sub("-", "—", data[
                    "name"])  # formats the player name to not have a normal dash as this breaks the code
                player_rank_emoji = ranks[data["rank"]]
                blue_team += f"\n[ {player_rank_emoji}{' '}{player_name}]"
            if len(blue_team) >= 1024:
                logging.debug(f"The red_team length is over 1024 even with links removed. The length is{len(blue_team)}")
                logging.info(f"Spectator player info below {blue_team}")
                blue_team = "Investigating this bug"


        # below embed is if DM, SDM, INTERVAL, or SCAP is selected
        if game_mode_no in [0, 12, 13, 15]:
            id_embeds[lobby_id] = (discord.Embed(title=f":flag_{region.lower()}: {lobby_name}",
                                       url=f"https://mgo2pc.com/game/{lobby_id}",
                                       description="",
                                       colour=0x2f3136)
                         .add_field(name=f"Map:", value=f"{map_name}", inline=True)
                         .add_field(name=f"Mode:", value=f"{game_mode}", inline=True)
                         .add_field(name=f" ", value=f" ", inline=False)
                         .add_field(name=f"**Players({players}/{lobby_player_limit})**", value=f"{player_info}",
                                    inline=True)
                         .add_field(name=f"{invisible_space}", value=f"{player_info2}", inline=True)
                         .set_image(url=map_thumbnail))

        # below embed checks if team -1, sneaking_team, and assigning team has no data
        elif player_team_negative_1 == "" and sneaking_team == "" and assigning_team_1 == "" and assigning_team_2 == "":
            id_embeds[lobby_id] = (discord.Embed(title=f":flag_{region.lower()}: {lobby_name}",
                                       url=f"https://mgo2pc.com/game/{lobby_id}",
                                       description="",
                                       colour=0x2f3136)
                         .add_field(name=f"Map:", value=f"{map_name}", inline=True)
                         .add_field(name=f"Mode:", value=f"{game_mode}", inline=True)
                         .add_field(name="**Players**", value=f"{players}/{lobby_player_limit}", inline=True)
                         .add_field(name=f" ", value=f" ", inline=False)
                         .add_field(name=f"Blue Team", value=f"{blue_team}", inline=True)
                         .add_field(name=f"Red Team", value=f"{red_team}", inline=True)
                         .add_field(name=f"Spectators", value=f"{spectators}")
                         .set_image(url=map_thumbnail))

        # if assigning team has a value then the below embed is produced
        elif assigning_team_1 != "":
            id_embeds[lobby_id] = (discord.Embed(title=f":flag_{region.lower()}: {lobby_name}",
                                       url=f"https://mgo2pc.com/game/{lobby_id}",
                                       description="",
                                       colour=0x2f3136)
                         .add_field(name=f"{invisible_space}Map:{invisible_space}",
                                    value=f"{invisible_space}{map_name}", inline=True)
                         .add_field(name=f"Mode:", value=f"{game_mode}", inline=True)
                         .add_field(name=f"**Players**", value=f"{players}/{lobby_player_limit}", inline=True)
                         .add_field(name=f"\u2001", value=f"\u2001", inline=False)
                         .add_field(name=f"Blue Team", value=f"{blue_team}", inline=True)
                         .add_field(name=f"Red Team", value=f"{red_team}", inline=True)
                         .add_field(name=f"Spectators", value=f"{spectators}")
                         .add_field(name=f"Assigning Teams", value=f"{assigning_team_1}")
                         .add_field(name=f"Assigning Teams", value=f"{assigning_team_2}", inline=True)
                         .set_image(url=map_thumbnail))


        elif game_mode_no == 4:
            id_embeds[lobby_id] = (discord.Embed(title=f":flag_{region.lower()}: {lobby_name}",
                                       url=f"https://mgo2pc.com/game/{lobby_id}",
                                       description="",
                                       colour=0x2f3136)
                         .add_field(name=f"Map:", value=f"{map_name}", inline=True)
                         .add_field(name=f"Mode:", value=f"{game_mode}", inline=True)
                         .add_field(name="**Players**", value=f"{players}/{lobby_player_limit}", inline=True)
                         .add_field(name=f"", value=f"", inline=False)
                         .add_field(name=f"Blue Team", value=f"{blue_team}", inline=True)
                         .add_field(name=f"Red Team", value=f"{red_team}", inline=True)
                         .add_field(name=f"Spectators", value=f"{spectators}")
                         .add_field(name=f"Sneaking Team", value=f"{sneaking_team}")
                         .set_image(url=map_thumbnail))

        else:
            id_embeds[lobby_id] =(discord.Embed(title=f"{invisible_space}:flag_{region.lower()}: {lobby_name}",
                                       url=f"https://mgo2pc.com/game/{lobby_id}",
                                       description="",
                                       colour=0x2f3136)
                         .add_field(name=f"Map:", value=f"{map_name}", inline=True)
                         .add_field(name=f"Mode:", value=f"{game_mode}", inline=True)
                         .add_field(name=f"**Players**", value=f"{players}/{lobby_player_limit}", inline=True)
                         .add_field(name=f"", value=f"", inline=False)
                         .add_field(name=f"Your Instructor", value=f"{sneaking_team}", inline=False)
                         .add_field(name=f"Blue Team", value=f"{blue_team}", inline=True)
                         .add_field(name=f"Red Team", value=f"{red_team}", inline=True)
                         .add_field(name=f"Spectators", value=f"{spectators}")
                         .set_image(url=map_thumbnail))

    return id_embeds
