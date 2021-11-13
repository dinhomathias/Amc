While you program your bot and while the bot is running there can be several things that can go wrong. This page gives an overview on how you can handle those situations.

# Exceptions

In `python-telegram-bot`, all Telegram-related errors are encapsulated in the `TelegramError` exception class and its subclasses, located in [`telegram.error`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.error.html) module.

Any error, including `TelegramError`, that is raised in one of your handlers (or while calling `get_updates` in the `Updater`), is forwarded to all registered error handlers, so you can react to them. You can register an error handler by calling `Dispatcher.add_error_handler(callback)`, where `callback` is a function that takes the `update` and `context`. `update` will be the update that caused the error (or `None` if the error wasn't caused by an update, e.g. for [[Jobs|Extensions-–-JobQueue]]) and `context.error` the error that was raised.

**Example:** You're trying to send a message, but the user blocked the bot. An `Unauthorized` exception, a subclass of `TelegramError`, will be raised and delivered to your error handler, so you can delete it from your conversation list, if you keep one.

**Note:** The error handler might be only your last resort - of course you can also handle Exceptions as they occur. Only uncaught exceptions are forwarded to the error handler.

## Example

For an example on how an error handler might look like, please head over to the [examples directory](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples).

# Logging

In case you don't have an error handler registered, PTB will *log* any unhandled exception.
For logging, PTB uses Pythons [`logging` module](https://docs.python.org/3/library/logging.html).
To set up logging to standard output, you can write
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```
at the beginning of your script. If you want debug logs instead:
```python
logger.setLevel(logging.DEBUG)
```
`python-telegram-bot` makes some more verbose log entries on the `logging.DEBUG` level that might be helpful when you're trying to debug your bot.

Note that also some 3rd party libraries that `python-telegram-bot` uses, make log entries in the same manner. For example, if you don't want to see the logs of the `APScheduler` library about your `JobQueue` jobs being scheduled, you can specify the logging level of `APScheduler` as follows:

```python
import logging

aps_logger = logging.getLogger('apscheduler')
aps_logger.setLevel(logging.WARNING)
```

# Warnings

In contrast to exceptions, warnings usually don't indicate that something already did go wrong, but rather that something *could* go wrong or at least could be improved.
Warnings issued by `python-telegram-bot` are encapsulated in `PTBUserWarnang` or one of the subclasses, located in the [`telegram.warnings` module](https://python-telegram-bot.readthedocs.io/en/stable/telegram.warnings.html).
This allows you to easily handle the warnings using Pythons [`warnings` library](https://docs.python.org/3/library/warnings.html).
For example, if you don't want to miss any deprecation warning during development, you can tell Python to turn every such warning issued by PTB into an exception via

```python
import warnings
from telegram.error import PTBUserWarning

warnings.filterwarnings("error", category=PTBDeprecationWarning)
```