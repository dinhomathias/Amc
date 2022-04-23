## Table of contents

Add this in the end …

# Structural changes & Deprecations

## Removed features

We made a cut and dropped all deprecated functionality. Most importantly, this includes the old-style handler API, which was deprecated in [[Version 12|Transition-guide-to-Version-12.0#context-based-callbacks]]. 

## `asyncio`

The deepest structural change is introducing the `asyncio` module into `python-telegram-bot`.

> [`asyncio`](https://docs.python.org/3/library/asyncio.html) asyncio is a library to write concurrent code using the `async`/`await` syntax.

What does this mean and why do we care?

`python-telegram-bot` is a library with the main purpose of communicating with the Telegram Bot API via web requests.
When making web requests, your code usually spends a *lot* of time with - waiting.
Namely, waiting for a response from Telegram.
The same holds for many so-called input-output (I/O) tasks.
Instead of sitting around, your program could already do other stuff in that time.

So far, PTB has build on the [`threading`](https://docs.python.org/3/library/threading.html) library to overcome this issue.

`asyncio` is a modern alternative to `threading` that comes with multiple advantages.
Covering those or an introduction to how using `asyncio` works, is sadly beyond the scope of this transition guide or the PTB resources in general.
Searching for `python asyncio introduction` or `python asyncio vs threading` in your favorite search engine will yield numerous results that will help you get up to speed.

The main points of what `asyncio` changed in PTB are:

* PTB doesn't use threads anymore. It is also not thread safe!
* All API methods of `telegram.Bot` are now coroutine functions, i.e. you have to `await` them
* All handler & job callbacks must be coroutine functions, i.e. you need to change `def callback(update, context)` to `async def callback(update, context)`.
* the `run_async` parameter of the handlers was replaced by the `block` parameter, which has a similar functionality. More details on this can be found on [[this page|here be link]].
* The method `Dipsatcher.run_async` doesn't exist anymore. Something that comes close to its functionality is `Application.create_task` (more on `Application` below). More details on this can be found on [[this page|here be link]].
* All methods that make calls coroutines or preform any I/O bound tasks are now coroutine functions.
This includes all abstract methods of `BasePersistence`. Listing them all here would be too long. When in doubt, please consult the documentation at [ReadTheDocs](https://python-telegram-bot.readthedocs.io).

##  Refinement of the public API

We've made an effort to make it more clear which parts of `python-telegram-bot` can be considered to be part of the public interface that users are allowed to use. To phrase it the other way around: Which parts are internals of `python-telegram-bot` are implementation details that might change without notice. Notably this means:

1. Only non-private modules are part of the public API and you should import classes & functions the way they are described in the docs. E.g. `from telegram.error import TelegramError` is fine, but `from telegram._message import Message` is strongly discouraged - use `from telegram import Message` instead.
2. We have removed the module `telegram.utils`. The parts of this module that we consider to be part of the public API have been moved into the modules `telegram.{helpers, request, warnings}`.

## `__slots__`

We introduced the usage of `__slots__` in v13.6, which can reduce memory usage and improve performance. In v14 we removed the ability to set custom attributes on all objects except for `ext.CallbackContext`. To store data, we recommend to use PTBs built-in mechanism for [storing data](Storing-bot,-user-and-chat-related-data) instead. If you want to add additional functionality to some class, we suggest to subclass it.

## Overall architecture

`ext.Updater` is no longer the entry point to a PTB program and we have replaced the `ext.Dispatcher` class with the new class `ext.Application`.

The `Application` is the new entry point to a PTB program and binds all its components together. The following diagram gives you an overview.

<details><summary>Click to show the diagram</summary>

![PTB v20 Architecture](https://gcdnb.pbrd.co/images/VYfQoTJBY1Mo.png?o=1)

</details>

When initializing an `Application`, many settings can be configured for the inidividual components.
In an effort to make this instantiation both clear and clean, we adopted the so-called [builder pattern](https://en.wikipedia.org/wiki/Builder_pattern).
This means that instead of passing arguments directly to `Application`, one creates a builder via `Application.builder()` and then specifies all required arguments via that builder.
Finally, the `Application` is created by calling `builder.build()`. A simple example is

```python
from telegram.ext import Application
application = Application.builder().token('TOKEN').build()
```

We hope that this design makes it easier for you to understand what goes where and also simplifies setups of customized solutions, e.g. if you want to use a custom webhook.

There is also a [[standalone wiki page|Builder-Pattern]] just about this topic.

# Changes for specific modules, classes & functions

## `telegram`

Previously some parts of `telegram.{error, constants}` where available directly via the `telegram` package - e.g. `from telegram import TelegramError`. These imports will no longer work. Only classes that directly reflect the official Bot API are now available directly via the `telegram` package. Constants and errors are available via the modules `telegram.{error, constants}` - e.g. `from telegram.error import TelegramError`.

### Several classes

Previously, some classes (like `telegram.{Message, User, Chat}`) had an attribute `bot` that was used for the shortcuts (e.g. `Message.reply_text`). This attribute was removed.
Instead, the new method `TelegramObject.{set, get}_bot()` are used.

### `telegram.ChatAction`

This class was removed as it is not part of the official Bot API. Use `telegram.constants.ChatAction` instead.

### `telegram.constants`

This module was rewritten from scratch. The constants are now grouped with the help of [Enums](https://docs.python.org/3/library/enum.html#enum.Enum).

### `telegram.Bot`

* The argument `media` of `Bot.edit_message_media` is now the first positional argument as specified by the Bot API.
* The argument `url` of `Bot.set_webhook` is now required as specified by the Bot API.
* The argument `description` of `Bot.set_chat_description` is now optional as specified by the Bot API.

### `telegram.EncryptedPassportElement`

The argument `hash` is now the second positional argument as specified by the Bot API.

### `telegram.error`

`telegram.error.Unauthorized` was replaced by `telegram.error.Forbidden`.
Moreover, `telegram.error.Forbidden` is now only raised if your bot tries to perform actions that it doesn't have enough rights for.
In case your bot token is invalid, `telegram.error.InvalidToken` is raised.

### `telegram.File`

* The `custom_path` parameter now also accepts `pathlib.Path` objects.
* Instead of returning the file path as string, it's now returned as `pathlib.Path` object.

### `telegram.ForceReply`

The argument `force_reply` was removed, since it *always* must be `True` anyway.

### `telegram.InlineQuery.answer`

If both parameters `current_offset` and `auto_pagination` are supplied, the method now raises a `ValueError` rather than a `TypeError`.

### `telegram.ParseMode`

This class was removed as it is not part of the official Bot API. Use `telegram.constants.ParseMode` instead.

### `telegram.PassportFile`

The argument `file_size` is now optional as specified by the Bot API.

### `telegram.ReplyMarkup`

This class was removed as it is not part of the official Bot API.

### `telegram.VoiceChat`

The argument `users` is now optional as specified by the Bot API.

## `telegram.ext`

### `BasePersistence`

#### `asyncio`

All abstract methods are now coroutine functions as implementations should be able to perform I/O tasks in a non-blocking way.

#### Data must be copyable

Any data passed to persistence will be copied with [`copy.deepcopy`](https://docs.python.org/3/library/copy.html#copy.deepcopy).
This requirement is in place to avoid race conditions.

#### Persisting `telegram.Bot` instances.

In [[Version 13|Transition-guide-to-Version-13.0]], we introduced a mechanism that replaces any `telegram.Bot` instance with a placeholder automatically *before* `update_*_data` was called and inserts the instance back into the return value of `get_*_data`. Unfortunately, this mechanism has proven to be unstable and also slow.

We have therefore decided to remove this functionality. `Bot` instances should still not be serialized, but handling this is now the responsibility of the specific implementation of `BasePersistence`. For example, `ext.PicklePersistence` uses the built-in functionality of the `pickle` module to achieve the same effect in a more reliable way.

More detailed information on this can be found in the documentation of `{Base, Pickle}Persistence`.

#### Return value of `get_{user, chat}_data`

`BasePersistence.get_{user, chat}_data` are no longer expected to return `collections.defaultdict`. Instead, they may return plain `dicts`.

#### Abstract methods

`BasePersistence` made a full transition to an abstract base class. This means that now all methods that a subclass should implement are marked as `abc.abstractmethod`. If e.g. you don't need `update_bot_data` because your persistence class is not supposed to store `bot_data`, you will still have to override that method, but you can simply make it `pass`.

#### `store_*_data`

The parameters & attributes `store_{user,chat,bot}_data` were removed. Instead, these settings were combined into the argument/attribute `store_data`, which accepts an instance of the new helper class [`telegram.ext.PersistenceInput`](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.persistenceinput.html#telegram-ext-persistenceinput).

Note that `callback_data` is now persisted by default.

### `CallbackContext`

* `CallbackContext.from_error` has a new optional argument `job`. When an exception happens inside a `ext.Job` callback, this parameter will be passed.
* Accordingly, the attribute `CallbackContext.job` will now also be present in error handlers if the error was caused by a `ext.Job`. 

### `ConversationHandler`

ConversationHandler now raises warnings for more handlers which are added in the wrong context/shouldn't be in the handler at all.

### `filters`

The `ext.filters` module was rewritten almost from scratch and uses a new namespace policy. The changes are roughly as follows:

1. `telegram.ext.Filters` no longer exists. Instead, use the module `telegram.ext.filters` directly. For example, `Filters.text` has to be replaced by `filters.TEXT`
2. Already instantiated filters that don't need arguments are now in `SCREAMING_SNAKE_CASE`, e.g. `filters.TEXT`. Filter *classes* that do need arguments to be used are now in `CamelCase`, e.g. `filters.User`.
3. For filters that are closely related, we now use a namespace class to group them. For example, `filters.Document` can not be used in `MessageHandler`. To filter for messages with *any* document attached, use `filters.Document.ALL` instead.

Moreover, filters are no longer callable. To check if a filter accepts an update, use the new syntax `my_filter.check_update(update)` instead.

### `JobQueue`

#### New arguments `{chat, user}_id`

All scheduling methods (`JobQueue.run_*`) have two new arguments `{chat, user}_id`, which allows to easily associate a user/chat with a job. By specifying these arguments, the corresponding ID will be available in the job callback via `context.job.{chat, user}_id`.

Moreover, `context.{char, user}_data` will be available. This has some subtile advantages over the previous workaround `job_queue.run_*(..., context=context.chat_data)` and we recommend using this new feature instead. 

#### `JobQueue.run_monthly`

Unfortunately, the `day_is_strict` argument was not working correctly (see [#2627](../issues/2627)) and was therefore removed. Instead, you cann now pass `day='last'` to make the job run on the last day of the month.

### `Job`

#### Removed the attribute `job_queue`

This was removed because if you have access to a job, then you also have access to either the `JobQueue` directly or at least a `CallbackContext` instance, which already contains the `job_queue`.

### `PicklePersistence`

* The argument `filename` was renamed to `filepath` and now also accepts a `pathlib.Path` object
* [Changes to `BasePersistence`](#basepersistence) also affect this class.

### `Updater`

The sole purpose of this class now is to fetch updates from Telegram. It now only accepts the arguments `bot` and `update_queue` and only has those attributes.

### `Application`/`Dispatcher`

#### `user/chat_data`

If you were modifying the `user/chat_data` of `Dispatcher` directly e.g. by doing `context.dispatcher.chat_data[id] = ...`, then this will now not work. [`Application.user/chat_data`](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.application.html#telegram.ext.Application.chat_data) is now read only. Note that `context.chat/user_data[key] = ...` will still work.
