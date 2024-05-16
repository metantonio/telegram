# Telegram Bot

This bot will verify the users, and give them access to certain files

## Installation

1) First you need to have Python installed. For most users, basic installation is enough: [Python 3.10.2](https://www.python.org/downloads/release/python-3102/). Download the windows installer (probably you have 64 bit system)

2) Install Libraries: execute `install_libs.bat` file. A `.env` file should be created

3) Configure .env file. If you don't know where to obtain the Gmail password for apps, keep reading. If you don't know how to obtain your Telegram Bot Token from @BotFather, keep reading.

4) Configure `contact.json` file, this contains the telegram usernames and their emails asociates, you must put the usernames and emails in the same format.

5) Configure `files.json` file, here you should have the name of the course and url files that you want to share


## Configure @BotFather in telegram

1) Search for @Botfather in Telegram

2) Start a conversation with BotFather by writing `/start`

3) Type `/newbot` and follow the prompts to set up a new bot. The BotFather will give you a token that you will use to authenticate your bot and grant it access to the Telegram API.

4) If your forgot your token, you can type `/token` to obtain it again. Remeber to put it in the `.env` file (not in .env.example)

5) Add the bot to your group, with admin access. Navigate to https://api.telegram.org/bot-token-/getUpdates   
Replace `-token-` with your actual token.

6) If everything is ok, you should check: 

## Configure Gmail Password for apps

1) Go to Gmail, and then to Managament Your Account

2) On the search bar type: `App passwords`. Probably will ass you for your actual password to enter.

3) Type a name to label this password, exmaple: `telegram-bot`. It will retrieve a password for apps, that you will keep safe and put it on the `.env` file, without the dashes (-)


# Run Server

Run just using `start.bat` file

