## ⚠️ Note

This transition guide is subject to changes as long as v20.0 is in pre-release mode.
Individual pre-releases for v20.0 will not get standalone transition guides.

Moreover, it's important to note that this transition guide will not cover every last one of the many smaller changes that came along with the bigger structural changes.
If you notice that some non trivial change is missing in here, feel free to add it.

## Table of contents

- [Transition Script](#transition-script)
- [Structural changes & Deprecations](#structural-changes---deprecations)
  * [Removed features](#removed-features)
  * [`asyncio`](#asyncio)
  * [Refinement of the public API](#refinement-of-the-public-api)
  * [`__slots__`](##__slots__)
  * [Overall architecture](#overall-architecture)
- [Changes for specific modules, classes & functions](#changes-for-specific-modules--classes---functions)
  * [`telegram`](#telegram)
    + [Several classes](#several-classes)
    + [Networking Backend](#networking-backend)
    + [`telegram.ChatAction`](#telegramchataction)
    + [`telegram.constants`](#telegramconstants)
    + [`telegram.Bot`](#telegrambot)
    + [`telegram.EncryptedPassportElement`](#telegramencryptedpassportelement)
    + [`telegram.error`](#telegramerror)
    + [`telegram.File`](#telegramfile)
    + [`telegram.ForceReply`](#telegramforcereply)
    + [`telegram.InlineQuery.answer`](#telegraminlinequeryanswer)
    + [`telegram.ParseMode`](#telegramparsemode)
    + [`telegram.PassportFile`](#telegrampassportfile)
    + [`telegram.ReplyMarkup`](#telegramreplymarkup)
    + [`telegram.VideoChat`](#telegramvideochat)
  * [`telegram.ext`](#telegramext)
    + [`BasePersistence`](#basepersistence)
      - [`asyncio`](#asyncio-1)
      - [Data must be copyable](#data-must-be-copyable)
      - [Persisting `telegram.Bot` instances.](#persisting-telegrambot-instances)
      - [Return value of `get_{user, chat}_data`](return-value-of-get_user-chat_data)
      - [Abstract methods](#abstract-methods)
      - [`store_*_data`](#store__data)
    + [`CallbackContext`](#callbackcontext)
    + [`ConversationHandler`](#conversationhandler)
    + [`filters`](#filters)
    + [`JobQueue`](#jobqueue)
      - [New arguments `{chat, user}_id`](#new-arguments-chat-user_id)
      - [`JobQueue.run_monthly`](#-jobqueuerun-monthly-)
    + [`Job`](#job)
      - [Removed the attribute `job_queue`](#removed-the-attribute-job_queue)
    + [`PicklePersistence`](#picklepersistence)
    + [`Updater`](#updater)
    + [`Application`/`Dispatcher`](#applicationdispatcher)
      - [`user/chat_data`](#userchat_data)

# Transition Script

We have prepared a script that is aimed at easing the transition for you.
Note that this script currently just does some regex-based search & replace take some of the transition work off your shoulders.
It is no way a supplement for reading this transition guide and manually adjusting your code base.
In addition to the script, we recommend using a language interpreter (e.g. `pylint`) and a static type checker (e.g. `mypy`) on your code base to minimize the trial-and-error time during transitioning at a minimum.

> Here be details

# Structural changes & Deprecations

## Removed features

We made a cut and dropped all deprecated functionality. Most importantly, this includes the old-style handler API, which was deprecated in [[Version 12|Transition-guide-to-Version-12.0#context-based-callbacks]], and the MessageQueue. 

## `asyncio`

The deepest structural change is introducing the `asyncio` module into `python-telegram-bot`.

> [`asyncio`](https://docs.python.org/3/library/asyncio.html) is a library to write concurrent code using the `async`/`await` syntax.

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
* the `run_async` parameter of the handlers was replaced by the `block` parameter, which has a similar functionality. More details on this can be found on [[this page|Concurrency]].
* The method `Dipsatcher.run_async` doesn't exist anymore. Something that comes close to its functionality is `Application.create_task` (more on `Application` below). More details on this can be found on [[this page|Concurrency]].
* All methods that make calls coroutines or preform any I/O bound tasks are now coroutine functions.
This includes all abstract methods of `BasePersistence`. Listing them all here would be too long. When in doubt, please consult the documentation at [ReadTheDocs](https://python-telegram-bot.readthedocs.io).

##  Refinement of the public API

We've made an effort to make it more clear which parts of `python-telegram-bot` can be considered to be part of the public interface that users are allowed to use. To phrase it the other way around: Which parts are internals of `python-telegram-bot` are implementation details that might change without notice. Notably this means:

1. Only non-private modules are part of the public API and you should import classes & functions the way they are described in the docs. E.g. `from telegram.error import TelegramError` is fine, but `from telegram._message import Message` is strongly discouraged - use `from telegram import Message` instead.
2. We have removed the module `telegram.utils`. The parts of this module that we consider to be part of the public API have been moved into the modules `telegram.{helpers, request, warnings}`.

## `__slots__`

We introduced the usage of `__slots__` in v13.6, which can reduce memory usage and improve performance. In v20 we removed the ability to set custom attributes on all objects except for `ext.CallbackContext`. To store data, we recommend to use PTBs built-in mechanism for [storing data](Storing-bot,-user-and-chat-related-data) instead. If you want to add additional functionality to some class, we suggest to subclass it.

## Overall architecture

`ext.Updater` is no longer the entry point to a PTB program and we have replaced the `ext.Dispatcher` class with the new class `ext.Application`.

The `Application` is the new entry point to a PTB program and binds all its components together. The following diagram gives you an overview.

<details><summary>Click to show the diagram</summary>

[[/assets/ptb_architecture.png]]

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

### Networking backend

Previously, the class `telegram.utils.request.Request` formed the networking backend of PTB.
This class has been removed.
Instead, there is the new module `telegram.request`, which contains an interface class `BaseRequest` as well as an implementation `HTTPXRequest` of that class via the `httpx` library.
By default, the `HTTPXRequest` class is used for the networking backend.
Advanced users may use a custom backend by implementing a custom subclass of `BaseRequest`.
See [[this page|Architecture]] for more information on that.

### `telegram.ChatAction`

This class was removed as it is not part of the official Bot API. Use `telegram.constants.ChatAction` instead.

### `telegram.constants`

This module was rewritten from scratch. The constants are now grouped with the help of [Enums](https://docs.python.org/3/library/enum.html#enum.Enum).

### `telegram.Bot`

* The class has a new argument `get_updates_request` in addition to `request` and the corresponding request instance will be used exclusively for calling `getUpdates`.
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

### `telegram.VideoChat`

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

We have prepared a script that will help you convert your v13 pickle-files into v20 pickle files.
Note that this script is a best-effort solution for a conversion - for some special cases, a conversion may not be possible without adjusting the v13 data before.

> Here be details

### `Updater`

The sole purpose of this class now is to fetch updates from Telegram. It now only accepts the arguments `bot` and `update_queue` and only has those attributes.

### `Application`/`Dispatcher`

#### `user/chat_data`

If you were modifying the `user/chat_data` of `Dispatcher` directly e.g. by doing `context.dispatcher.chat_data[id] = ...`, then this will now not work. [`Application.user/chat_data`](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.application.html#telegram.ext.Application.chat_data) is now read only. Note that `context.chat/user_data[key] = ...` will still work.