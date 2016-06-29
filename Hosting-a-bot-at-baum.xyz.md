## Introduction
Before you start, you need a working bot of your own creation. **Do not follow this tutorial just for testing one of our examples.** You can test bots on your own computer, there is no need for a hosting service to do that. 

**Note:** The topics **First Login** through **Start your bot** and **What to read next?** are probably the same for all Ubuntu based servers.

## Getting started

### Requesting an account
To host a bot with [baum](http://baum.xyz), you have to write their Telegram Bot at [@bothostingbot](https://telegram.me/bothostingbot) and follow a few instructions. Carefully read the rules and requirements. If you don't meet those, don't proceed. It is a free service run by volunteers, so please be respectful.

The bot will ask you to explain how you will use the service. Someone will read your request and (hopefully) approve it by hand, so give your best! This will take some time. Once you received your server information, you can proceed.

### First login
Your login details should contain
- The IP address of your server
- Your username (usually `root`)
- Your password

You should also receive some information on the type of server you got, including Operating System, RAM, storage and monthly traffic.

Once you received that information, you can connect to the server via SSH. 

#### Linux
Run the following command in the terminal and replace `<user>` with your username and `<ip>` with your servers IP address:

```
ssh <user>@<ip>
```

Confirm that you want to trust the host and enter the password if you are asked to do so.

#### Windows
Install [puTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) and start it. 

In the field *Host Name (or IP address)* enter the IP address of your server. As the connection type, select *SSH* and set *Port* to *22*. You can save these settings my entering a name in the field below *Saved Sessions* and clicking *Save*. Then, click *Open* and enter your username and password when asked to do so.

### Setup
First, install the Python package manager `pip` (replace `python-pip` with `python3-pip` if you want to use Python 3).
```
apt-get update && apt-get install python-pip
```

Now, install the `python-telegram-bot` library (replace `pip` with `pip3` if you're using Python 3):
```
pip install python-telegram-bot
```

Finally, confirm the installation (replace `python` with `python3` if you're using Python 3):
```
python -c "import telegram;print(telegram.__version__)"
```

### Upload your bot's files
Now you can upload your bot to the server. There are multiple ways to do that, one way is to use [FileZilla](https://filezilla-project.org/download.php?type=client). Install it (if you're on Linux, chances are you already have it) and start it. Open the *Server Manager* and create a new server with the button on the left. Give it a nice name, then go to the right and fill in the fields:

- *Server:* Your servers IP address
- *Port:* 22
- *Protocol:* SFTP
- *Connection type:* Normal
- *Username:* Your username
- *Password:* Your password

Now, click *Connect*. You will probably see the `/root` directory (your user's home directory) on the right and your local files on the left. Create a directory for your bot and upload all the files needed by your bot into that directory.

### Start your bot
To run your bot, connect to your server again via SSH (or go back to the connection) and `cd` into the directory you created. You could now immediately start the bot, but then it would stop working once you disconnect from the server. There are again many ways to make sure that doesn't happen, one way is to use `screen`. 

`screen` is called a "terminal multiplexer". It creates *virtual terminals* that you can attach to and detach from and that can run processes without you being logged in.

Create a new *screen* and attach to it:
```
screen -S mybot
```

Start the bot (replace `python` with `python3` if you're using Python 3):
```
python bot.py
```

Detach from the *screen* by holding *Ctrl* and pressing *A*, then *D*. You can now disconnect from the server by typing `exit` if you want. 

To re-attach to the *screen* after you logged back in:
```
screen -r mybot
```

## Donations
The baum.xyz-service runs on donations and volunteer work. If you found it useful and have some leftover money on your bank account, consider [a donation](http://baum.xyz/donate/) to help keeping the service free and available. Hosting servers is expensive.

## What to read next?
If you plan on hosting multiple bots on your server, it's recommended to use `virtualenv`. It allows you to install and upgrade python modules via `pip` for one project, without worrying how it affects other projects on the server. Read [this external article](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for more information.

Learn about how to use a webhook for your bot in [this article](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks).

You might also read the article on [Performance Optimizations](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Performance-Optimizations) if you didn't read it yet. Note that baum.xyz hosts their servers in Germany with a good connection to the Bot API servers, so you can safely ignore the second part of that article about choosing a server location.