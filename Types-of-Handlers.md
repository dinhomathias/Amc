A `Handler` is an instance derived from the base class [telegram.ext.Handler](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.handler.html#telegram.ext.Handler) which is responsible for the routing of different kinds of updates (text, audio, inlinequery, button presses, ...) to their _corresponding callback function_ in your code.
For example, if you want your bot to respond to the command `/start`, you can use a [CommandHandler](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.commandhandler.html) that maps the input to a callback named `my_start_callback`:
```
def my_start_callback(bot, update):
    update.message.reply_text("Welcome to my awesome bot!")

...

dispatcher.add_handler(CommandHandler("start", my_start_callback))```