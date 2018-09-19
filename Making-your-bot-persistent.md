In Vx.x we added a persistence mechanism to `telegram.ext`. This wiki is set up to help you understand and set up persistence for your bots.

# What can become persistent?
The persistence structure is designed to make `chat_data`, `user_data` and `ConversationHandler`'s states persistent.
`Job`'s and the `job_queue` is not supported because the serialization of callbacks is too unstable to reliably make persistent for broad user-cases. For a snippet on how to save and restore a basic `job_queue` see [here](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#save-and-load-jobs-using-pickle).

# Included persistence classes
three classes concerning persistence in bots have been added. 
[BasePersistence](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.basepersistence.html) - Is an interface class for persistence classes. If you create your own persistence classes to maintaint a database-connection for example, you must inherit from `BasePersistence`
[PicklePersistence](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.picklepersistence.html) - Uses pickle files to make the bot persistent.
[DictPersistence](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.dictpersistence.html) - Uses in memory dicts and easy conversion to and from JSON to make the bot persistent.

# 3rd party persistence classes
If you want to create your own persistence class, please carfully read the docs on [BasePersistence](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.basepersistence.html). It will tell you what methods you need to overwrite. If you;ve written a persistence class that could be of use to others (e.g. a general one covering all types of data). Please add it  below.

# What do I need to change?
To make your bot persistent you need to know the following.

- Create a persistence object (e.g. `my_persistence = PicklePersistence(filename='my_file')`)
- Construct Updater with the persistence (`Updater('TOKEN', persistence=my_persistence)`)

This is enough for to make `user_data` and `chat_data` persistent.
To make a conversationhandler persistent (save states between bot restarts)
`ConversationHandler(<no change>, persistent=True, name='my_name')`
If you want a conversationhandler to be persisten you **MUST NAME IT**. persistent is `False` by default.
Adding these arguments and adding the conversationhandler to a persistence-aware updater/dispatcher will make it persistent.
 