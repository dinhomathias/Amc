## Table of contents

Add this in the end …

# New functionality

Apart from all the refactorings & deprecations explained below, v14 also contains some new functionality. Notable are

* `Filters.update.edited` provides a shortcut for `(Filters.update.edited_message | Filters.update.edited_channel_post)`

# Structural changes & Deprecations

## Removed features

We made a cut and dropped all deprecated functionality. Most importantly, this includes the old-style handler API, which was deprecated in [[Version 12|Transition-guide-to-Version-12.0#context-based-callbacks]]. 

##  Refinement of the public API

We've made an effort to make it more clear which parts of `python-telegram-bot` can be considered to be part of the public interface that users are allowed to use. To phrase it the other way around: Which parts are internals of `python-telegram-bot` or implementation details that might change without notice. Notably this means:

1. Only non-private modules are part of the public API and you should import classes & functions the way they are described in the docs. E.g. `from telegram.error import TelegramError` is fine, but `from telegram._message import Message` is strongly discouraged - use `from telegram import Message` instead.
2. We have removed the module `telegram.utils`. The parts of this module that we consider to be part of the public API have been moved into the modules `telegram.{helpers, request, warnings}`.

## `__slots__`

We introduced the usage of `__slots__` in v13.6, which can reduce memory usage and improve performance. In v14 we removed the ability to set custom attributes on all objects except for `ext.CallbackContext`. To store data, we recommend to use PTBs built-in mechanism for [storing data](Storing-bot,-user-and-chat-related-data) instead. If you want to add additional functionality to some class, we suggest to subclass it.

## Instantiation of `Updater` and `Dispatcher`

`Updater` and `Dispatcher` had a large number of arguments many of which were mutually exclusive, and it was not always clear which argument was e.g. intended for the `Updater` and which was passed along to the `Dispatcher` or even the `Bot`.
In an effort to make the instantiation of `Updater` and `Dispatcher` more clear, we adopted the so-called [builder pattern](https://en.wikipedia.org/wiki/Builder_pattern).
This means that instead of passing arguments directly to `Updater`/`Dispatcher`, one now creates a builder via `Updater/Dispatcher.builder()` and then specifies all required arguments via that builder.
Finally, the `Updater/Dispatcher` is created by calling `builder.build()`. A simple example is

```python
from telegram.ext import Updater
updater = Updater.builder().token('TOKEN').build()
```

We hope that this change makes it easier for you to understand what goes where and also simplifies setups of customized solutions, e.g. if you want to use a custom webhook.  

# Changes for specific modules, classes & functions

## `telegram`

Previously some parts of `telegram.{error, constants}` where available directly via the `telegram` package - e.g. `from telegram import TelegramError`. These imports will no longer work. Only classes that directly reflect the official Bot API are now available directly via the `telegram` package. Constants and errors are available via the modules `telegram.{error, constants}` - e.g. `from telegram.error import TelegramError`.

### `telegram.Bot`

* The argument `media` of `Bot.edit_message_media` is now the first positional argument as specified by the Bot API.
* The argument `url` of `Bot.set_webhook` is now required as specified by the Bot API.
* The argument `description` of `Bot.set_chat_description` is now optional as specified by the Bot API.

### `telegram.EncryptedPassportElement`

The argument `hash` is now the second positional argument as specified by the Bot API.

### `telegram.File`

* The `custom_path` parameter now also accepts `pathlib.Path` objects.
* Instead of returning the file path as string, it's now returned as `pathlib.Path` object.

### `telegram.ForceReply`

The argument `force_reply` was removed, since it *always* must be `True` anyway.

### `telegram.InlineQuery.answer`

If both parameters `current_offset` and `auto_pagination` are supplied, the method now raises a `ValueError` rather than a `TypeError`.

### `telegram.PassportFile`

The argument `file_size` is now optional as specified by the Bot API.

### `telegram.VoicChat`

The argument `users` is now optional as specified by the Bot API.

## `telegram.ext`

### `BasePersistence`

#### Abstract methods

`BasePersistence` made a full transition to an abstract base class. This means that now all methods that a subclass should implement are marked as `abc.abstractmethod`. If e.g. you don't need `update_bot_data` because your persistence class is not supposed to store `bot_data`, you will still have to override that method, but you can simply make it `pass`.

#### `store_*_data`

The parameters & attributes `store_{user,chat,bot}_data` were removed. Instead, these settings were combined into the argument/attribute `store_data`, which accepts an instance of the new helper class `telegram.ext.PersistenceInput`.

Note that `callback_data` is now persisted by default.

### `CallbackContext`

* `CallbackContext.from_error` has a new optional argument `job`. When an exception happens inside a `ext.Job` callback, this parameter will be passed.
* Accordingly, the attribute `CallbackContext.job` will now also be present in error handlers if the error was caused by a `ext.Job`. 

### `ConversationHandler`

ConversationHandler now raises warnings for more handlers which are added in the wrong context/shouldn't be in the handler at all.

### `JobQueue.run_monthly`

Unfortunately, the `day_is_strict` argument was not working correctly (see [#2627](../issues/2627)) and was therefore removed. Instead, you cann now pass `day='last'` to make the job run on the last day of the month. 

### `PicklePersistence`

* The argument `filename` was renamed to `filepath` and now also accepts a `pathlib.Path` object
* [Changes to `BasePersistence`](#basepersistence) also affect this class.

### `Updater`

In addition to the changes described [above](#instantiation-of-updater-and-dispatcher)

* the attribute `user_sig_handler` was renamed to `user_signal_handler`
* the attributes `job_queue` and `persistence` were removed. Instead, you can access them via `updater.dispatcher.{job_queue, persistence}`.
