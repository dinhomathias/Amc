### Introduction
You will need a VPS (or dedicated server) first. Check out the list at [Where to host Telegram Bots](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Where-to-host-Telegram-Bots#vps) if you don't have one already.

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

Detach from the *screen* by holding <kbd>CTRL</kbd> and pressing <kbd>A</kbd>, then <kbd>D</kbd>. You can now disconnect from the server by typing `exit` if you want. 

To re-attach to the *screen* after you logged back in:
```
screen -r mybot
```
or
```
screen -d -m mybot
```

## What to read next?
If you plan on hosting multiple bots on your server, it's recommended to use `virtualenv`. It allows you to install and upgrade Python modules via `pip` for one project, without worrying how it affects other projects on the server. Read [this external article](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for more information.

Learn about how to use a webhook for your bot in [this article](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks).

You might also read the article on [Performance Optimizations](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Performance-Optimizations) if you didn't read it yet.