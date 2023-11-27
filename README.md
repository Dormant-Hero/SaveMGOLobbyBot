
# ![logo 4185b845](https://github.com/Dormant-Hero/SaveMGOLobbyBot/assets/79374258/11f754cb-aa63-4e83-adc5-6d780e334e11)

This bot provides a live feed into a discord channel of all the games being played in SaveMGO2/Metal Gear Online 2 (the online component to MGS4). It is a **work in progress** as a result it currently does not have error handling.

<br>

# Setting up the Discord Bot

There are 2 ways to setup my bot. You can either run it on my server (may change my mind if heavy traffic one day but would try to warn people in advance via the bot) or you can run this bot of your own server.

## Hosting from your own server

Copy the .py files and run the bot in your chosen code editor or server host as you would with any other bot. As far as I am aware message intentions are all that is required but the official bot I have has message, server member, and presence enabled. 
The only thing you are going to need to set this up is your bot token. Please see the image below: 

![img.png](img.png)


## Using my server for the bot

Simply click this [link](https://discord.com/api/oauth2/authorize?client_id=1175813240605913190&permissions=355344&scope=bot%20applications.commands) to invite the Discord bot to your server. That is it you have a lobby bot 😎.

![img_1.png](img_1.png)


## Usage

You can follow this [video guide](https://youtu.be/bWCSD36b4AE) or follow the instructions below in relation to usage.

Once the bot is on your server create the discord channel you want the lobbies to be sent on (you can give it any name). 

![img_2.png](img_2.png)

Once done I recommend you check the permissions of the channel and/or just ensure the bot has the necessary permissions. In my case I am using the below:

![img_5.png](img_5.png)

![img_11.png](img_11.png)

![img_6.png](img_6.png)

![img_7.png](img_7.png)

![img_8.png](img_8.png)

![img_9.png](img_9.png)

![img_10.png](img_10.png)

Now the permissions are set we just need to copy the channel id into the command /set_channel_id so the bot knows where 
you would like the lobby embeds posted for your server.

![img_12.png](img_12.png)

![img_13.png](img_13.png)

![img_14.png](img_14.png)

With our channel assigned simply type !startand you should find some nice lobby embeds being produced 😏.

![img_15.png](img_15.png)

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


