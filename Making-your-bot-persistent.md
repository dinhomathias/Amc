In V12.0b1 we added a persistence mechanism to `telegram.ext`. This wiki page is there to help you understand and set up persistence for your bots.

## What can become persistent?
The persistence structure is designed to make `bot_data`, `chat_data`, `user_data` and `ConversationHandler`'s states persistent.
`Job`'s and the `job_queue` is not supported because the serialization of callbacks is too unstable to reliably make persistent for broad user-cases. For a snippet on how to save and restore a basic `job_queue` see [here](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#save-and-load-jobs-using-pickle).

## Included persistence classes
Three classes concerning persistence in bots have been added.  
[BasePersistence](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.basepersistence.html) - Is an interface class for persistence classes. If you create your own persistence classes to maintain a database-connection for example, you must inherit from `BasePersistence`  
[PicklePersistence](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.picklepersistence.html) - Uses pickle files to make the bot persistent.  
[DictPersistence](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.dictpersistence.html) - Uses in memory dicts and easy conversion to and from JSON to make the bot persistent. Note that this class is mainly intended as starting point for custom persistence
        classes that need to JSON-serialize the stored data before writing them to file/database and does *not* actually write any data to file/database.

## 3rd party persistence classes
If you want to create your own persistence class, please carefully read the docs on [BasePersistence](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.basepersistence.html). It will tell you what methods you need to overwrite. 

If you've written a persistence class that could benefit others (e.g. a general one covering all types of data), please add it below.

## What do I need to change?
To make your bot persistent you need to do the following.

- Create a persistence object (e.g. `my_persistence = PicklePersistence(filename='my_file')`)
- Construct Updater with the persistence (`Updater('TOKEN', persistence=my_persistence, use_context=True)`)

This is enough to make `user_data`, `bot_data` and `chat_data` persistent.
To make a conversation handler persistent (save states between bot restarts) you **must name it** and set `persistent` to `True`.
Like `ConversationHandler(<no change>, persistent=True, name='my_name')`. `persistent` is `False` by default.
Adding these arguments and adding the conversation handler to a persistence-aware updater/dispatcher will make it persistent.
 