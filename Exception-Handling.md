In `python-telegram-bot`, all Telegram-related errors are encapsulated in the `TelegramError` exception class and its subclasses, located in [`telegram.error`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.error.html) module.

Any error, including `TelegramError`, that is raised in one of your handlers (or while calling `get_updates` in the `Updater`), is forwarded to all registered error handlers, so you can react to them. You can register an error handler by calling `Dispatcher.add_error_handler(callback)`, where `callback` is a function that takes the `update` and `context`. `update` will be the update that caused the error (or `None` if the error wasn't caused by an update, e.g. for [Jobs](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-–-JobQueue)) and `context.error` the error that was raised.

**Example:** You're trying to send a message, but the user blocked the bot. An `Unauthorized` exception, a subclass of `TelegramError`, will be raised and delivered to your error handler, so you can delete it from your conversation list, if you keep one.

**Note:** The error handler might be only your last resort - of course you can also handle Exceptions as they occur. Only uncaught exceptions are forwarded to the error handler.

## Example

For an example on how an error handler might look like, please head over to the [examples directory](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples).