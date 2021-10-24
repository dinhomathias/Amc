In V12.0b1 we added a persistence mechanism to `telegram.ext`. This wiki page is there to help you understand and set up persistence for your bots.

- [What can become persistent?](#what-can-become-persistent-)
- [Included persistence classes](#included-persistence-classes)
- [3rd party persistence classes](#3rd-party-persistence-classes)
- [What do I need to change?](#what-do-i-need-to-change-)
- [Storing Bots](#storing-bots)

## What can become persistent?
* The persistence structure is designed to make `bot_data`, `chat_data`, `user_data`, `ConversationHandler`'s states and `ExtBot.callback_data_cache` persistent.
* `Job`'s and the `job_queue` is not supported because the serialization of callbacks is too unstable to reliably make persistent for broad user-cases. However, the current `JobQueue` backend [APScheduler](https://apscheduler.readthedocs.io/en/stable/) has its own persistence logic that you can leverage.
* For a special note about `Bot` instances, see [below](#storing-bots)

## Included persistence classes
Three classes concerning persistence in bots have been added.  
* [BasePersistence](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.basepersistence.html) - Is an interface class for persistence classes. If you create your own persistence classes to maintain a database-connection for example, you must inherit from `BasePersistence`  
* [PicklePersistence](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.picklepersistence.html) - Uses pickle files to make the bot persistent.  
* [DictPersistence](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.dictpersistence.html) - Uses in memory dicts and easy conversion to and from JSON to make the bot persistent. Note that this class is mainly intended as starting point for custom persistence
        classes that need to JSON-serialize the stored data before writing them to file/database and does *not* actually write any data to file/database.

## 3rd party persistence classes
Instead of manually handling a database to store data, consider implementing a subclass of `BasePersistence`. This allows you to simply pass an instance of that subclass to the `Updater/Dispatcher` and let PTB handle the loading, updating & storing of the data!

If you want to create your own persistence class, please carefully read the docs on [BasePersistence](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.basepersistence.html). It will tell you what methods you need to overwrite. 

If you've written a persistence class that could benefit others (e.g., a general one covering all types of data), it would be great if you linked it here or even better made it available in [ptbcontrib](https://github.com/python-telegram-bot/ptbcontrib).

## What do I need to change?
To make your bot persistent you need to do the following.

- Create a persistence object (e.g. `my_persistence = PicklePersistence(filename='my_file')`)
- Construct `Updater` with the persistence (`Updater('TOKEN', persistence=my_persistence, use_context=True)`). If you don't use the `Updater` class, you can pass the persistence directly to the `Dispatcher`.

This is enough to make `user_data`, `bot_data`, `chat_data` and `ExtBot.callback_data_cache` persistent.
To make a conversation handler persistent (save states between bot restarts) you **must name it** and set `persistent` to `True`.
Like `ConversationHandler(<no change>, persistent=True, name='my_name')`. `persistent` is `False` by default.
Adding these arguments and adding the conversation handler to a persistence-aware updater/dispatcher will make it persistent.

## Refreshing at runtime

If your persistence reads the data from an external database, the entries in this database could change at runtime. This is the case in particular, if the entries in the database are created by a 3rd party service independently of your bot. If you want to make sure that the data in `context.user/chat/bot_data` are always up-to-date, your persistence class should implement the methods `refresh_bot/chat/user_data`. Those will be called when in update comes in, before any of your callbacks are called.

## Storing Bots

As of v13, persistence will automatically try to replace `telegram.Bot` instances by [`REPLACED_BOT`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.basepersistence.html#telegram.ext.BasePersistence.REPLACED_BOT) and
insert the bot set with [`set_bot`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.basepersistence.html#telegram.ext.BasePersistence.set_bot) upon loading of the data. This is to ensure that
changes to the bot apply to the saved objects, too. For example, you might change the [[default values|Adding-defaults-to-your-bot]] used by the bot. If you change the bots token, this may
lead to e.g. `Chat not found` errors. For the limitations on replacing bots see
[`replace_bot`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.basepersistence.html#telegram.ext.BasePersistence.replace_bot) and [`insert_bot`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.basepersistence.html#telegram.ext.BasePersistence.insert_bot).

This is relevant e.g., if you store Telegram objects like `Message` in `bot/user/chat_data`, as some of them have a `bot` attribute, which holds a reference to the `Dispatchers` bot.
 