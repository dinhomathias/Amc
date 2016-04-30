In python-telegram-bot, we have error handlers that take care of all `TelegramError` exceptions that are risen, so you can react to them.
Example: You're trying to send a message, but the user blocked the bot. An `Unauthorized` exception, a subclass of `TelegramError`, will be raised and delivered to your error handler, so you can delete it from your conversation list, if you keep one.


Example code:

```python
from telegram.error import TelegramError, Unauthorized, TimedOut, NetworkError

def error_callback(bot, update, error):
    try:
        raise error
    except Unauthorized:
        # remove update.message.chat_id from conversation list
    except TimedOut:
        # handle slow connection problems
    except NetworkError:
        # handle other connection problems
    except TelegramError:
        # handle all other telegram related errors

dispatcher.addErrorHandler(error_callback)
```

### Other exceptions
If a handler raises an uncaught exception that is no `TelegramError` (e.g. an `IndexError`), the exception will be caught and logged by the `Dispatcher`, so that the bot does not crash but you still have an indication of it and can address the issue. To take advantage of this, it is imperative to set up the `logging` module.


Example code:

```python
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
```