
# ![logo 4185b845](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/11f754cb-aa63-4e83-adc5-6d780e334e11)

This bot provides a live feed into a discord channel of all the games being played in SaveMGO2/Metal Gear Online 2 (the online component to MGS4). It is a **work in progress** as a result it currently does not have error handling.

<br>

# Setting up the Discord Bot

There are 2 ways to setup my bot. You can either run it on my server (may change my mind if heavy traffic one day but would try to warn people in advance via the bot) or you can run this bot of your own server.

## Hosting from your own server

Copy the .py files and run the bot in your chosen code editor or server host as you would with any other bot. As far as I am aware message intentions are all that is required but the official bot I have has message, server member, and presence enabled. 
The only thing you are going to need to set this up is your bot token. Please see the image below: 

![img](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/65580f79-3a6b-4112-928c-0f047686558b)


## Using my server for the bot

Simply click this [link](https://discord.com/api/oauth2/authorize?client_id=1175813240605913190&permissions=355344&scope=bot%20applications.commands) to invite the Discord bot to your server. That is it you have a lobby bot 😎.

![img_1](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/ceb8d64d-f99f-4d69-a37c-637a3fa6c184)



## Usage

You can follow this [video guide](https://youtu.be/bWCSD36b4AE) or follow the instructions below in relation to usage.

Once the bot is on your server create the discord channel you want the lobbies to be sent on (you can give it any name). 

![img_2](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/076782f4-dafd-4420-870b-bbdc1470a942)


Once done I recommend you check the permissions of the channel and/or just ensure the bot has the necessary permissions. In my case I am using the below:

![img_5](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/da96d941-6887-4da7-9bc3-6eb66c44df04)

![img_11](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/3c18701c-976b-4aac-ad00-d6f411f74133)

![img_6](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/da477644-10c3-4294-98bd-44be5a68c64a)

![img_7](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/df776870-e01e-40f8-a1a3-f16f3e9f478b)

![img_8](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/56ee4390-4657-49d3-a177-2e2c5bd1ae2c)

![img_9](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/7170c369-3453-4a60-ae6e-d01b7ee24065)

![img_10](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/73820bf2-f820-40be-917c-106c64591379)

Now the permissions are set we just need to copy the channel id into the command /set_channel_id so the bot knows where 
you would like the lobby embeds posted for your server.

![img_12](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/efffeaf8-4b3b-4734-963d-8d01e424d428)

![img_13](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/4022ea8d-0144-4414-bcaf-e970a89ac1e0)

![img_14](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/03b89e0b-a9d0-469c-9365-ba10cac708d5)

With our channel assigned simply type !startand you should find some nice lobby embeds being produced 😏.

![img_15](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/c4325ad2-bb87-48bc-b13c-b2ee9c7d5ff6)


### Note if your running this of your own server

You can download the custom emojis like the ones you see in the below image from the SaveMGO discord @ discord.gg/mgo2pc 
then host them in your server or others with the bot located inside of them.

**Custom Emojis in the embed**

![image](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/bc605b6a-d7db-48fb-9e62-33c51a94d0f9)

These images below shows you how to receive custom emoji codes for any emoji. Post the emoji from one of the servers your server is in 
and at a backslash \ in-front of it as per the below:

![image](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/1747a361-5b66-451b-836d-8eea4970ae5a)

You will then receive this emoji code which can be pasted into the data.py.

![image](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/cd029f73-c088-432e-8732-7324aeacde4d)


