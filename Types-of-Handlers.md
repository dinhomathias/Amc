A `Handler` is an instance derived from the base class [telegram.ext.Handler](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.handler.html#telegram.ext.Handler) which is responsible for the routing of different kinds of updates (text, audio, inlinequery, button presses, ...) to their _corresponding callback function_ in your code.

For example, if you want your bot to respond to the command `/start`, you can use a [CommandHandler](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.commandhandler.html) that maps this user input to a callback named `start_callback`:
```
def start_callback(update, context):
    update.message.reply_text("Welcome to my awesome bot!")

...

dispatcher.add_handler(CommandHandler("start", start_callback))
```

## CommandHandlers with arguments

It is also possible to work with parameters for commands offered by your bot. Let's extend the `start_callback` with some arguments so that the user can provide additional information in the same step:

```
def start_callback(update, context):
    user_says = " ".join(context.args)
    update.message.reply_text("You said: " + user_says)

...

dispatcher.add_handler(CommandHandler("start", start_callback))
```

Sending "/start Hello World!" to your bot will now split everything after /start separated by the space character into a list of words and pass it on to the `args` parameter of `context`: `["Hello", "World!"]`. We join these chunks together by calling `" ".join(context.args)` and echo the resulting string back to the user.

### Deep-Linking start parameters
The argument passing described above works exactly the same when the user clicks on a deeply linked start URL, like this one:

[https://t.me/roolsbot?start=Hello_World!](https://t.me/roolsbot?start=Hello_World!)

Clicking this link will open your Telegram Client and show a big START button. When it is pressed, the URL parameters "Hello_World!" will be passed on to the `args` of your context object.

Note that since telegram doesn't support spaces in deep linking parameters, you will have to manually split the single `Hello_World` argument, into `["Hello", "World!"]` (using `context.args[0].split('_')` for example)

You also have to pay attention to the maximum length accepted by Telegram itself. As stated in the [documentation](https://core.telegram.org/bots#deep-linking) the maximum length for the start parameter is 64.

Also, since this is an URL parameter, you have to pay attention on how to correctly pass the values in order to  avoid passing URL reserved characters. Consider the usage of `base64.urlsafe_b64encode`.

## Pattern matching: The RegexHandler

Warning: Regexhandler is being deprecated. See our [Transition guide](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Transition-guide-to-Version-12.0) for more information.

For more complex inputs you can employ the [telegram.ext.RegexHandler](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.regexhandler.html), which internally uses the `re`-module to match textual user input with a supplied pattern.

Keep in mind that for extracting URLs, #Hashtags, @Mentions, and other Telegram entities, there's no need to parse them with a `RegexHandler` because the Bot API already sends them to us with every update. Refer to [this snippet](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#message-entities) to learn how to work with entities instead.


This tutorial only covers some of the available handlers (for now). Refer to the documentation for all other types: https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.html#handlers
