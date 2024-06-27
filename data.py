# The below are images of all the maps
map_choices = {
    1: ["FF", "https://media.discordapp.net/attachments/817184487061454928/1182774563780702289/FF.jpg?ex=6585eba6&is=657376a6&hm=7dd8ba9c2b76ba6f1b134e33701826274b227ceb9cec383a8b73661f2295bf90&=&format=webp"],
    2: ["AA", "https://media.discordapp.net/attachments/817184487061454928/1182771569039261746/AA.jpg?ex=6585e8dc&is=657373dc&hm=d2d977f4353f941130fed86dbbc5779fab0798430a57df9a1a74cdece49aafcb&=&format=webp"],
    3: ["UU", "https://media.discordapp.net/attachments/817184487061454928/1182774540917551276/UU.jpg?ex=6585eba1&is=657376a1&hm=94700dd2183208a53a89a7d4951b1febfe63090f9f9e5ca8e972637951948da1&=&format=webp"],
    4: ["GG", "https://media.discordapp.net/attachments/817184487061454928/1182774563495481434/GG.jpg?ex=6585eba6&is=657376a6&hm=57287066c7b1d157db4b93994595e511e345aeba4c7404aa9ebd518056a754ec&=&format=webp"],
    5: ["CC", "https://media.discordapp.net/attachments/817184487061454928/1182774564342730762/CC.jpg?ex=6585eba7&is=657376a7&hm=97f168fd323413c881c0150d624f04f9fe71e9a497c637d264a4041ab32d0b23&=&format=webp"],
    6: ["HH", "https://media.discordapp.net/attachments/817184487061454928/1182774563227062382/HH.jpg?ex=6585eba6&is=657376a6&hm=53edec6e8aa1969e3715ebd922416bbab789aa3d21c4afdf5b0a674d7cbdea04&=&format=webp"],
    7: ["BB", "https://media.discordapp.net/attachments/817184487061454928/1182776276143046716/BB.jpg?ex=6585ed3f&is=6573783f&hm=5bac5632a334011f245107a3366555fc14787882e1e8db2e92b27f5895eb2f12&=&format=webp"],
    8: ["TT", "https://media.discordapp.net/attachments/817184487061454928/1182774541227937902/TT.jpg?ex=6585eba1&is=657376a1&hm=2b281b482529828363235832d9ff71613059089a3b7de162bd53358ede16bc30&=&format=webp"],
    9: ["RR", "https://media.discordapp.net/attachments/817184487061454928/1182774539457933393/RR.jpg?ex=6585eba1&is=657376a1&hm=7a37f76c18bf73c02572802e37e7446b0759ea6198435fe1def7458ac5f98717&=&format=webp"],
    10: ["SS", "https://media.discordapp.net/attachments/817184487061454928/1182774539004936302/SS.jpg?ex=6585eba0&is=657376a0&hm=b56dc87f2bdbddd43b58c38d6c369f4aae0d6050d8c699d1a6de0f07320645a5&=&format=webp"],
    11: ["II", "https://media.discordapp.net/attachments/817184487061454928/1182776276478607442/II.jpg?ex=6585ed3f&is=6573783f&hm=063bf342f134d6bcb80f9b669825b6bdfe9192fd5a48f4c5d8e0e3cddd8ce121&=&format=webp"],
    12: ["MM", "https://media.discordapp.net/attachments/817184487061454928/1182774565001236573/MM.jpg?ex=6585eba7&is=657376a7&hm=9cdd5b55f83ac3010150577b22d63a6a06f99f25cfe41c28e7460e8f073c8cc9&=&format=webp"],
    13: ["WW", "https://media.discordapp.net/attachments/817184487061454928/1182774540284219534/WW.jpg?ex=6585eba1&is=657376a1&hm=234266a14aa87bc63bccc5a8f0d660948d272b83c2b87f39279c8d6ee9e51693&=&format=webp"],
    14: ["VV", "https://media.discordapp.net/attachments/817184487061454928/1182774540632326195/VV.jpg?ex=6585eba1&is=657376a1&hm=9b6ff2e9cccd411091097ec8fcaed5fa44ee3a3622637ab0a7189fc9ae4a9fb3&=&format=webp"],
    15: ["OO", "https://media.discordapp.net/attachments/817184487061454928/1182774564653117572/OO.jpg?ex=6585eba7&is=657376a7&hm=700e059edc812a2947858770070fa96261d1b7cb582dcf24b06bb3a0b7a67210&=&format=webp"],
    16: ["Unknown Map16", "https://mgo2pc.com/games"],
    17: ["DD", "https://media.discordapp.net/attachments/817184487061454928/1182774564070113280/DD.jpg?ex=6585eba6&is=657376a6&hm=9d095a45abdd8c071b081d86fe1da4d4dcbac43b5eb5e162300c99a060e6116d&=&format=webp"],
    18: ["LL", "https://media.discordapp.net/attachments/817184487061454928/1182774565290651749/LL.jpg?ex=6585eba7&is=657376a7&hm=31017a1aee3d2089e0f53dad47c846fc67ccb2b3a9a88f87b4453d98365f6ea6&=&format=webp"],
    19: ["PP", "https://media.discordapp.net/attachments/817184487061454928/1182774540007374929/PP.jpg?ex=6585eba1&is=657376a1&hm=dae9a7a09c370f38b2bcb7455d1adb234e1c17627c05ae30385d3de114ab28ff&=&format=webp"],
    20: ["QQ", "https://media.discordapp.net/attachments/817184487061454928/1182774539734765629/Q.jpg?ex=6585eba1&is=657376a1&hm=3c289725d6142efd61b00200111f82d72c081ea1a2cd3eceed314c587fb440dd&=&format=webp"],
    21: ["JJ", "https://media.discordapp.net/attachments/817184487061454928/1182774565626200185/JJ.jpg?ex=6585eba7&is=657376a7&hm=97b901866166a52fbeea7d60907b2a6ab9fff5967a00b878281938e9d1a3367c&=&format=webp"],
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
    "locked": "<:lock:1180872870684012664>",
    "unlocked": ""
}

dp = {
    0: "",
    2: "<:dp:1180861589289701466>",
    3: " Message Marko aka dormant hero as something unexpected occured",
    4: "<:hsonly:1181375450602287145>",
    32: " (Alternative map)"
}

host = "<:host:1180901051545702411>"

lobbies = {
    5: "Contact Dormant if you see this. This should be a normal lobby",
    15: " <:nohs2:1183914594255777802>",
    20: "Contact Dormant if you see this."
}
