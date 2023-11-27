import requests

# Global variables to store API data
all_lobby_data = None
total_players = None
all_lobby_ids = []

# below function is imported and called in other files to make an api request
def run_api_request():
    global all_lobby_data, total_players, all_lobby_ids
    all_lobby_ids = []
    response = requests.get(url="https://mgo2pc.com/api/v1/games")
    response.raise_for_status()
    data = response.json()
    all_lobby_data = data["data"]["lobbies"]
    total_players = data["data"]["players"]  # Number of players online including not in a match
    for data in all_lobby_data:
        all_lobby_ids.append(data["id"])

run_api_request()


def get_lobby_Data():
    return all_lobby_data

def get_total_players():
    return total_players

def get_all_lobby_ids():
    return all_lobby_ids

