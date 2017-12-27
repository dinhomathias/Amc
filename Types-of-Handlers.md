A `Handler` is an instance derived from the base class [telegram.ext.Handler](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.handler.html#telegram.ext.Handler) which is responsible for the routing of different kinds of updates (text, audio, inlinequery, button presses, ...) to their _corresponding callback function_ in your code.

For example, if you want your bot to respond to the command `/start`, you can use a [CommandHandler](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.commandhandler.html) that maps this user input to a callback named `start_callback`:
```
def start_callback(bot, update):
    update.message.reply_text("Welcome to my awesome bot!")

...

dispatcher.add_handler(CommandHandler("start", start_callback))
```

## CommandHandlers with arguments

It is also possible to work with parameters for commands offered by your bot. Let's extend the `start_callback` with some arguments so that the user can provide additional information in the same step:

```
def start_callback(bot, update, args):
    user_says = " ".join(args)
    update.message.reply_text("You said: " + user_says)

...

dispatcher.add_handler(CommandHandler("start", start_callback, pass_args=True))```

Sending "/start Hello World!" to your bot will now split everything after /start separated by the space character into a list of words and pass it on to the `args` parameter of `start_callback`: `["Hello", "World!"]`. We join these chunks together by calling `" ".join(args)` and echo the resulting string back to the user.

### Deep-Linking start parameters
The argument passing described above works exactly the same when the user clicks on a deeply linked start URL, like this one:

https://t.me/roolsbot?start=Hello%20World!

Clicking this link will open your Telegram Client and show a big START button. When it is pressed, the URL parameters "Hello World!" will be passed on to the `args` of your /start callback.


## Pattern matching: The RegexHandler

For more complex inputs you can employ the [telegram.ext.RegexHandler](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.regexhandler.html), which internally uses the `re`-module to match textual user input with a supplied pattern.

A quick example:
```

```

Keep in mind that for extracting URLs, #Hashtags, @Mentions, and other Telegram entities, there's no need to parse them with a `RegexHandler` because the Bot API already sends them to us with every update. Refer to [this snippet](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#message-entities) to learn how to work with entities instead.


To learn about all 
