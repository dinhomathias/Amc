## Pure Telegram Bot API

The Bot API is exposed via the [`telegram.Bot`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html) class.
The methods are the `snake_case` equivalents of the methods described in the official [Telegram Bot API](https://core.telegram.org/bots/api).
The exact `camelCase` method names as in the Telegram docs are also available for your convenience.
For example, `telegram.Bot.send_message` is the same as `telegram.Bot.sendMessage`.
All the classes of the Bot API can also be found in the `telegram` module, e.g. the `Message` class is available as [`telegram.Message`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.message.html).

To generate an Access Token, you have to talk to [BotFather](https://t.me/botfather) and follow a few simple steps (described [here](https://core.telegram.org/bots#6-botfather)).

For full details see the official Telegram documentation at [Bots: An introduction for developers](https://core.telegram.org/bots).

#### Hello, Telegram!

To get a feeling for the API and how to use it with `python-telegram-bot`, please a new Python file.

We first want to create an instance of the `telegram.Bot` and check that the credentials are correct.
Please paste the following code into your file.
`'TOKEN'` should be replaced by the API token you received from `@BotFather`

```python
import asyncio
import telegram


async def main():
    bot = telegram.Bot("TOKEN")
    async with bot:
        print(await bot.get_me())


if __name__ == '__main__':
    asyncio.run(main())
```

Here we simply call the API method [getMe](https://core.telegram.org/bots/api#getme).
The `async with bot:` ensures that PTB can properly acquire and release resources.
If you run the file you should get an output along the lines

```pycon
>>> python main.py
{"first_name": "Toledo's Palace Bot", "username": "ToledosPalaceBot"}
```

So far so good.
Now we can try and actually do something - let's send a message.

However, bots can't initiate conversations with users.
A user must either add them to a group or send them a message first.
People can use ``telegram.me/<bot_username>`` links or username search to find your bot.

Because of above note, we'll have to first send a message to the bot.
If we've done that, we can fetch the update by replacing the `main` in our file with

```python
async def main():
    bot = telegram.Bot("TOKEN")
    async with bot:
        print(await bot.get_updates()[0])
```

The output should now look something like this (we abbreviated the output a bit):

```pycon
>>> python main.py
{'update_id': 218946040, 'message': {'message_id': 23833, 'date': 1626017436, 'text': 'Hi!', 'chat': {'type': 'private', 'last_name': 'Doe', 'username': 'JohnDoe', 'id': 1234567890, 'first_name': 'John'}, 'from': {'last_name': 'Doe', 'username': 'JohnDoe', 'id': 1234567890, 'is_bot': False, 'language_code': 'de', 'first_name': 'John'}, ...}}
```

We copy the chat id, here `1234567890`.
Note that you can access it also as `updates[0].message.from_user.id`, because `updates[0]` is an instance of the `Update` class.
Now that we have the chat ID, we can send a message by again adjust the `main`:

```python

```python
async def main():
    bot = telegram.Bot("TOKEN")
    async with bot:
        await bot.send_message(text='Hi John!', chat_id=1234567890)
```

## Beyond the pure API

That's all very nice, but usually you want your bot to actually react to more complex user input. That is, you want to build a chat-bot. `python-telegram-bot` offers a powerful extension module called `telegram.ext` that takes a lot of work off your shoulders. You can find an introduction at the [[Tutorial: Your first bot|Extensions-–-Your-first-Bot]].