In `python-telegram-bot`, all Telegram-related errors are encapsulated in the `TelegramError` exception class and its subclasses, located in [`telegram.error`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.error.html) module.

Any `TelegramError`, that is raised in one of your handlers (or while calling `get_updates` in the `Updater`), is forwarded to all registered error handlers, so you can react to them. You can register an error handler by calling `Dispatcher.add_error_handler(callback)`, where `callback` is a function that takes the `update` and `context`. `update` will be the update that caused the error and `context.error` the `TelegramError` that was raised.

Example: You're trying to send a message, but the user blocked the bot. An `Unauthorized` exception, a subclass of `TelegramError`, will be raised and delivered to your error handler, so you can delete it from your conversation list, if you keep one.

**Note:** The error handler might be only your last resort - of course you can also handle Exceptions as they occur. Only uncaught exceptions are forwarded to the error handler.

Here is an example code that uses all current subclasses of `TelegramError`:

```python
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)

def error_callback(update, context):
    try:
        raise context.error
    except Unauthorized:
        # remove update.message.chat_id from conversation list
    except BadRequest:
        # handle malformed requests - read more below!
    except TimedOut:
        # handle slow connection problems
    except NetworkError:
        # handle other connection problems
    except ChatMigrated as e:
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        # handle all other telegram related errors

dispatcher.add_error_handler(error_callback)
```

Here are some examples that would cause a `BadRequest` error to be raised:
```python
>>> bot.leave_chat(chat_id=<invalid chat id>)
[...]
telegram.error.BadRequest: Chat not found

>>> bot.answer_callback_query(<invalid query id>)
[...]
telegram.error.BadRequest: Query_id_invalid

>>> bot.get_file(<invalid file id>)
[...]
telegram.error.BadRequest: Invalid file id

>>> bot.edit_message_text(chat_id, "sample old message")
[...]
telegram.error.BadRequest: Message is not modified

>>> bot.send_message(chat_id, 'a'*40960)
[...]
telegram.error.BadRequest: Message is too long
```

For the last one you can check if your message is too long by comparing with `telegram.constants.MAX_MESSAGE_LENGTH`. There is something similar for captions: `telegram.constants.MAX_CAPTION_LENGTH`.

### Other exceptions

If a handler raises an uncaught exception that is no `TelegramError` (e.g. an `IndexError`), the exception will be caught and logged by the `Dispatcher`, so that the bot does not crash but you still have an indication of it and can address the issue. To take advantage of this, it is imperative to set up the `logging` module.

Example code to set up the `logging` module:

```python
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
```