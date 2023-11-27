from data import map_choices, game_modes, ranks
import re
import discord
from api_data import get_lobby_Data
import logging

def lobby_embed():
    embed = []
    all_lobby_data = get_lobby_Data()
    # A for loop that splits
    for lobby in all_lobby_data:
        all_player_data = lobby["players"]  # All player data from this lobby
        lobby_name = lobby["name"] #
        current_game = lobby["currentGame"]
        map_no = lobby["games"][current_game][1]
        map_name = map_choices[map_no][0]
        map_thumbnail = map_choices[map_no][1]
        game_mode_no = lobby["games"][current_game][0]
        game_mode = game_modes[game_mode_no]
        players = len(all_player_data)  # Players in the lobby
        lobby_player_limit = lobby["maxPlayers"]
        region = lobby["location"]
        lobby_id = lobby["id"]
        invisible_space = f"<:invisible:1177474192782929970>{' '}"  # Note special invisible characters used for spacing as normal spaces do not work.
        player_info = "" # Used for game modes without teams to split the teams into 2 so the embed does not take up too much space.
        player_info2 = "" # Used for game modes without teams to split the teams into 2 so the embed does not take up too much space.
        count = 0 # Used with the for loop below to indicate how many players in a match for game modes without teams.
        spectators = ""
        player_team_negative_1 = "" # Unknown what this value is but it is in the code just in case.
        red_team = ""
        blue_team = ""
        sneaking_team = ""
        assigning_team_1 = ""
        assigning_team_2 = ""
        for data in all_player_data:
            player_name = re.sub("-", "—", data["name"]) # formats the player name to not have a normal dash as this breaks the code
            player_link = f"https://mgo2pc.com/profile/{re.sub(' ', '%20', data['name'])}" # Accounts for HTML URL encoding required
            player_rank_emoji = ranks[data["rank"]]
            team = data["team"]
            count += 1
            # Splits the player listing in half so the embed takes up less room
            # All the other appends below are just adding player information to variables to be used in the embed later
            if count <= lobby_player_limit / 2:
                player_info += f"\n[ {player_rank_emoji}{' '}{player_name}]({player_link})"
            else:
                player_info2 += f"\n[ {player_rank_emoji}{' '}{player_name}]({player_link})"
            if team == -2:
                spectators += f"\n[ {player_rank_emoji}{' '}{player_name}]({player_link})"
            elif team == -1:
                player_team_negative_1 += f"\n[ {player_rank_emoji}{' '}{player_name}]({player_link})"
            elif team == 0:
                red_team += f"\n[ {player_rank_emoji}{' '}{player_name}]({player_link})"
            elif team == 1:
                blue_team += f"\n[ {player_rank_emoji}{' '}{player_name}]({player_link})"
            elif team == 2:
                sneaking_team += f"\n[ {player_rank_emoji}{' '}{player_name}]({player_link})"
            elif team == int(-32) and count <= lobby_player_limit / 2:
                assigning_team_1 += f"\n[{player_rank_emoji}{' '}{player_name}]({player_link})"
            else:
                assigning_team_2 += f"\n[{player_rank_emoji}{' '}{player_name}]({player_link})"
        logging.basicConfig(filename="Character Length Log", encoding="utf-8", level=logging.DEBUG)

        # if field more than 1024 then logs data for player info for me to investigate why and apologises
        if len(player_info) > 1024:
            logging.debug(f"This is the length of player.info {len(player_info)} in lobby {lobby_name} {lobby_id}")
            logging.info(player_info)
            player_info = "Bugged. Admin will investigate. Sorry for any inconvenience caused"

        # if field more than 1024 then logs data for player info2 for me to investigate why and for now produce embed without a link
        if len(player_info2) > 1024:
            logging.debug(f"This is the length of player.info2 {len(player_info2)} in lobby {lobby_name} {lobby_id}")
            logging.info(player_info2)
            player_info2 = "Bugged. Admin will investigate. Sorry for any inconvenience caused"


        # if field more than 1024 then logs data for spectators for me to investigate why and apologises
        if len(spectators) > 1024:
            logging.debug(f"This is the length of spectators {len(spectators)} in lobby {lobby_name} {lobby_id}")
            logging.info(spectators)
            spectators = "Bugged. Admin will investigate. Sorry for any inconvenience caused"

        # if field more than 1024 then logs data for team-1 for me to investigate why and apologises
        if len(player_team_negative_1) > 1024:
            logging.debug(f"This is the length of player_team negative_1 {len(player_team_negative_1)} in lobby {lobby_name} {lobby_id}")
            logging.info(player_team_negative_1)
            player_team_negative_1 = "Bugged. Admin will investigate. Sorry for any inconvenience caused"

        # if field more than 1024 then logs data for red team for me to investigate why and apologises
        if len(red_team) > 1024:
            logging.debug(f"This is the length of red_team {len(red_team)} in lobby {lobby_name} {lobby_id}")
            logging.info(red_team)
            red_team = "Bugged. Admin will investigate. Sorry for any inconvenience caused"

        # if field more than 1024 then logs data for blue team for me to investigate why and apologises
        if len(blue_team) > 1024:
            logging.debug(f"This is the length of blue_team {len(blue_team)} in lobby {lobby_name} {lobby_id}")


        # if field more than 1024 then logs data for blue team for me to investigate why and apologises
        if len(sneaking_team) > 1024:
            logging.debug(f"This is the length of sneaking_team {len(sneaking_team)} in lobby {lobby_name} {lobby_id}")
            logging.info(sneaking_team)
            blue_team = "Bugged. Admin will investigate. Sorry for any inconvenience caused"

        # if field more than 1024 then logs data for assigning_team_1 for me to investigate why and apologises
        if len(assigning_team_1) > 1024:
            logging.debug(f"This is the length of assigning team 1 {len(assigning_team_1)} in lobby {lobby_name} {lobby_id}")
            logging.info(sneaking_team)
            blue_team = "Bugged. Admin will investigate. Sorry for any inconvenience caused"

        # if field more than 1024 then logs data for assigning_team_2 for me to investigate why and apologises
        if len(assigning_team_2) > 1024:
            logging.debug(f"This is the length of assigning team 2 {len(assigning_team_2)} in lobby {lobby_name} {lobby_id}")
            logging.info(sneaking_team)
            blue_team = "Bugged. Admin will investigate. Sorry for any inconvenience caused"


        # below embed is if DM, SDM, INTERVAL, or SCAP is selected
        if game_mode_no in [0, 12, 13, 15]:
            embed.append(discord.Embed(title=f":flag_{region.lower()}: {lobby_name}",
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
            embed.append(discord.Embed(title=f":flag_{region.lower()}: {lobby_name}",
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
            embed.append(discord.Embed(title=f":flag_{region.lower()}: {lobby_name}",
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
            embed.append(discord.Embed(title=f":flag_{region.lower()}: {lobby_name}",
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
            embed.append(discord.Embed(title=f"{invisible_space}:flag_{region.lower()}: {lobby_name}",
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

    return embed
