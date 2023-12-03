# The below are images of all the maps
map_choices = {
    1: ["FF", "https://mgo2pc.com/static/1.313e65f6.jpg"],
    2: ["AA", "https://mgo2pc.com/static/2.1f42fd70.jpg"],
    3: ["UU", "https://mgo2pc.com/static/3.acfe8925.jpg"],
    4: ["GG", "https://mgo2pc.com/static/4.56232fe5.jpg"],
    5: ["CC", "https://mgo2pc.com/static/5.8fc5c935.jpg"],
    6: ["HH", "https://mgo2pc.com/static/6.2ca6d5ef.jpg"],
    7: ["BB", "https://mgo2pc.com/static/7.56c7ca18.jpg"],
    8: ["TT", "https://mgo2pc.com/static/8.b173b311.jpg"],
    9: ["RR", "https://mgo2pc.com/static/9.87b1a791.jpg"],
    10: ["SS", "https://mgo2pc.com/static/10.2b53accf.jpg"],
    11: ["II", "https://mgo2pc.com/static/11.a1411d3e.jpg"],
    12: ["MM", "https://mgo2pc.com/static/12.9e336964.jpg"],
    13: ["WW", "https://mgo2pc.com/static/13.d5597515.jpg"],
    14: ["VV", "https://mgo2pc.com/static/14.737092a2.jpg"],
    15: ["OO", "https://mgo2pc.com/static/15.08259399.jpg"],
    16: "",
    17: ["DD", "https://mgo2pc.com/static/17.7df3d363.jpg"],
    18: ["LL", "https://mgo2pc.com/static/18.27179fc1.jpg"],
    19: ["PP", "https://mgo2pc.com/static/19.34274f74.jpg"],
    20: ["QQ", "https://mgo2pc.com/static/20.cff13b73.jpg"],
    21: ["JJ", "https://mgo2pc.com/static/21.cc66b1a5.jpg"],
    22: ["Unknown Map", "https://mgo2pc.com/games"]  # Set this up for when an unknown map appears in the api
}

# All the possible modes that can be produced from the API the bot connects to
game_modes = {
    0: "DM",
    1: "TDM",
    2: "RES",
    3: "CAP",
    4: "SNE",
    5: "BASE",
    6: "BOMB",
    7: "TSNE",
    10: "CT",
    11: "CLAN CT",
    12: "SDM",
    13: "INT",
    15: "SCAP",
    16: "RACE",
    17: "Unknown Game Mode"  # Set this up as a game mode for when the api produces something unknown
}

# The below is just for my reference
# teams = {
#     -2: "Spectator",
#     -1: "team -1", # I do not know what this is yet.
#     0: "Red Team",
#     1: "Blue Team",
#     2: "Sneaking Team",
#     -32: "Assigning Team",
# }

# The below are all the emoji/animal ranks for the lobby listing. You will have to replace these with new listings
# for this functionality in a new discord server.
ranks = {
    0: "<:user:1177784682142761011>", # Used for no rank or when an unknown rank is obtained from the API
    1: "<:foxhound:942128442344882208>",
    2: "<:fox:942128442344878120>",
    3: "<:doberman:942128441849937951>",
    4: "<:hound:942128442277761115>",
    5: "<:crocodile:942128441883500636>",
    6: "<:eagle:942128442185502760>",
    7: "<:jaws:1177211465707556884>",
    8: "<:waterbear:942128442307137626>",
    9: "<:sloth:942128442005139457>",
    10: "<:flyingsquirrel:942128442235838534>",
    11: "<:pigeon:942128442416168961>",
    12: "<:owl:942128442311344258>",
    13: "<:tsuchinoko:942128442323927040>",
    14: "<:snake:942128442118393907>",
    15: "<:kerotan:942128442319716362>",
    16: "<:gako:942128442223263744>",
    17: "<:chameleon:942128441933828188>",
    18: "<:chicken:942128442411987025>",
    19: "<:bear:942128442361675826>",
    20: "<:tortoise:942128442349064212>",
    21: "<:bee:942128442407809104>",
    22: "<:rat:942128442290356254>",
    23: "<:fightingfish:942128441887698995>",
    24: "<:komododragon:942128442441359380>",
    25: "<:articskua:942128442399420466>",
    26: "<:killerwhale:942128442298732595>",
    27: "<:elephant:942128442223239239>",
    28: "<:cuckoo:942128442340696165>",
    29: "<:hog:942151016583942204>",
    30: "<:bigboss:1177217415797538866>",
    31: "<:theboss:1177217595246649344>",
    32: "<:patriot:1179446860423901224>",
    40: "<:octopus:1177217906120085644>",
    41: "<:gecko:1177968165762904075>",
    42: "<:panda:1177967282501197884>",
    43: "<:puma:1177968511281278976>",
    44: "<:scorpion:1177968072980713554>",
    45: "<:wolf:1177968356234641448>",
    46: "<:mantis:1177966582677385317>",
    47: "<:alien:1177968011202801736>",
    48: "<:leopard:1177967914045943881>",
    49: "<:panther:1177970112591052871>",
    51: "<:dev:1177981901517099048>",
    52: "<:ocelot:1177220081894297680>",
}

password_emoji = {
    "locked": "<:locked:1180559329611485285>",
    "unlocked": "<:unlocked:1180560763593691256>"
}

dp = {
    0: "",
    2: "<:dp:1063213449116668034>",
    3: "something unexpected. Take a screenshot and please inform me (Dormant Hero)."
}