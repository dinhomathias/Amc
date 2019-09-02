Sometimes you need to temporarily store some information about the current user and/or chat for later use. An example of this would be a survey bot that asks the user a series of questions one after another and saves them to your database when all answers are collected. 
# `user_data` and `chat_data`
The `telegram.ext` framework provides a built-in solution for this common task. To understand how it works, let's take a look at a naïve solution using a global variable. In case you're in a hurry, you can also [**jump straight to the explanation**](#explanation).

## Bad Example
The following complete example bot provides a very simple key/value storage. When you use the `/put` command to store a value, it returns an ID which you can use with the `/get` command to retrieve the stored value.

It uses a global dictionary named `all_user_data` that maps a user ID to a `dict` that represents the user specific storage.

```python
from uuid import uuid4
from telegram.ext import Updater, CommandHandler

all_user_data = dict()

def put(update, context):
    """Usage: /put value"""
    # Generate ID and seperate value from command
    key = str(uuid4())
    value = update.message.text.partition(' ')[2]

    user_id = update.message.from_user.id

    # Create user dict if it doesn't exist
    if user_id not in all_user_data:
        all_user_data[user_id] = dict()

    # Store value
    user_data = all_user_data[user_id]
    user_data[key] = value

    update.message.reply_text(key)

def get(update, context):
    """Usage: /get uuid"""
    # Seperate ID from command
    key = update.message.text.partition(' ')[2]

    user_id = update.message.from_user.id

    # Load value
    try:
        user_data = all_user_data[user_id]
        value = user_data[key]
        update.message.reply_text(value)

    except KeyError:
        update.message.reply_text('Not found')

if __name__ == '__main__':
    updater = Updater('TOKEN', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('put', put))
    dp.add_handler(CommandHandler('get', get))

    updater.start_polling()
    updater.idle()
```

If you read the code carefully, you might have noticed that the code that gets the current `user_data` from `all_user_data` is [repeated](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) in both callbacks.

## Good Example
```python
from uuid import uuid4
from telegram.ext import Updater, CommandHandler

def put(update, context):
    """Usage: /put value"""
    # Generate ID and seperate value from command
    key = str(uuid4())
    value = update.message.text.partition(' ')[2]

    # Store value
    context.user_data[key] = value

    update.message.reply_text(key)

def get(update, context):
    """Usage: /get uuid"""
    # Seperate ID from command
    key = update.message.text.partition(' ')[2]

    # Load value
    try:
        value = context.user_data[key]
        update.message.reply_text(value)

    except KeyError:
        update.message.reply_text('Not found')

if __name__ == '__main__':
    updater = Updater('TOKEN', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('put', put))
    dp.add_handler(CommandHandler('get', get))

    updater.start_polling()
    updater.idle()
```

**Note the following differences:**
- The global variable `all_user_data` was removed
- The repeated code to get the storage of the current user was removed
- The code to ensure that the storage exists was removed
- Both the `put` and `get` functions use context.user_data

### Explanation
By using `context.user_data` in any `Handler` callback, you have access to a user-specific `dict`.

*Every time the bot receives a message*, the handler for that message finds (or creates) the `user_data` of the user who sent the message. This dictionary is *shared across all handlers* of the bot.

#### What about `chat_data`?
`chat_data` works in the exact same way as `user_data`, except it is managed per *chat* instead of every *user*. Use `context.chat_data` to get access to this dict.

#### Notes & Tips
- **Everything is stored in memory.** This means that all `user_data` and `chat_data` is deleted when the bot process ends. If you don't want this, have a look at the [persistent page](Making-your-bot-persistent).
- Empty `user_data` and `chat_data` dictionaries are automatically deleted from memory after the update is processed.
 - If not empty, `user_data` and `chat_data` will be kept until the process ends.
- `user_data` and `chat_data` are different dictionaries even for private chats.
- You can not assign a new value to `user_data` or `chat_data`. Instead of `user_data = {}` and `user_data = other_dict`, use `user_data.clear()` and/or `user_data.update(other_dict)` respectively.
