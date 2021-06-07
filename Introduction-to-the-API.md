## Pure Telegram Bot API

The Bot API is exposed via the [`telegram.Bot`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html) class. The methods are the snake_case equivalents of the methods described in the official [Telegram Bot API](https://core.telegram.org/bots/api). The exact camelCase method names as in the Telegram docs are also available for your convenience. So for example `telegram.Bot.send_message` is the same as `telegram.Bot.sendMessage`. All the classes of the Bot API can also be found in the `telegram` module, e.g. the `Message` class is available as [`telegram.Message`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.message.html).

To generate an Access Token, you have to talk to [BotFather](https://t.me/botfather) and follow a few simple steps (described [here](https://core.telegram.org/bots#6-botfather)).

For full details see the official Telegram documentation at [Bots: An introduction for developers](https://core.telegram.org/bots).

#### Hello, Telegram!

To get a feeling for the API and how to use it with `python-telegram-bot`, **please open a Python command line** and follow the next few steps.

First, create an instance of the `telegram.Bot`. `'TOKEN'` should be replaced by the API token you received from `@BotFather`:

```python
>>> import telegram
>>> bot = telegram.Bot(token='TOKEN')
```

To check if your credentials are correct, call the [getMe](https://core.telegram.org/bots/api#getme) API method:

```python
>>> print(bot.get_me())
{"first_name": "Toledo's Palace Bot", "username": "ToledosPalaceBot"}
```

**Note:** Bots can't initiate conversations with users. A user must either add them to a group or send them a message first. People can use ``telegram.me/<bot_username>`` links or username search to find your bot.

## Beyond the pure API

That's all very nice, but usually you want your bot to actually react to some user input. That is, you want to build a chat-bot. `python-telegram-bot` offers a powerful extension module called `telegram.ext` that takes a lot of work of your shoulders. You can find an introduction at the [Tutorial: Your first bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-–-Your-first-Bot).