Sometimes you need to temporarily store some information about the current user and/or chat for later use. An example of this would be a survey bot that asks the user a series of questions one after another and saves them to your database when all answers are collected. 

# `bot_data`, `user_data` and `chat_data`

The `telegram.ext` framework provides a built-in solution for this common task. Let's jump straight to an example:

```python
from uuid import uuid4
from telegram.ext import Updater, CommandHandler

def put(update, context):
    """Usage: /put value"""
    # Generate ID and separate value from command
    key = str(uuid4())
    # We don't use context.args here, because the value may contain whitespaces
    value = update.message.text.partition(' ')[2]

    # Store value
    context.user_data[key] = value
    # Send the key to the user
    update.message.reply_text(key)

def get(update, context):
    """Usage: /get uuid"""
    # Seperate ID from command
    key = context.args[0]

    # Load value and send it to the user
    value = context.user_data.get(key, 'Not found')
    update.message.reply_text(value)

if __name__ == '__main__':
    updater = Updater('TOKEN', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('put', put))
    dp.add_handler(CommandHandler('get', get))

    updater.start_polling()
    updater.idle()
```

## Explanation
By using `context.user_data` in any `Handler` callback, you have access to a user-specific `dict`.

*Every time the bot receives a message*, the handler for that message finds (or creates) the `user_data` of the user who sent the message. This dictionary is *shared across all handlers* of the bot.

## What about `bot_data` and `chat_data`?
`chat_data` works in the exact same way as `user_data`, except it is managed per *chat* instead of every *user*. Use `context.chat_data` to get access to this dict. As of version 12.4 `bot_data` is provided as well and works in the exact same way as `user_data`, except it's a single dictionary for your bot. Use `context.bot_data` to get access to this dict.

## Notes & Tips
- **Everything is stored in memory.** This means that all `bot_data`, `user_data` and `chat_data` is deleted when the bot process ends. If you don't want this, have a look at the [persistence page](Making-your-bot-persistent).
 - If not empty, `bot_data`, `user_data` and `chat_data` will be kept until the process ends.
- `user_data` and `chat_data` are different dictionaries even for private chats.
- You can not assign a new value to `bot_data`, `user_data` or `chat_data`. Instead of `user_data = {}` and `user_data = other_dict`, use `user_data.clear()` and/or `user_data.update(other_dict)` respectively.

## Chat Migration
If a group chat migrates to supergroup, its chat id will change. Since the `chat_data` dicts are stored *per chat id* you'll need to transfer the data to the new id. Here are the two situations you may encounter:

### Status Updates sent by Telegram
When a group migrates, Telegram will send an update that just states the new info. In order to catch those, simply define a corresponding handler:

```python
def chat_migration(update, context):
    m = update.message
    dp = context.dispatcher # available since version 12.4

    # Get old and new chat ids
    old_id = m.migrate_from_chat_id or m.chat_id
    new_id = m.migrate_to_chat_id or m.chat_id

    # transfer data, if old data is still present
    if old_id in dp.chat_data:
        dp.chat_data[new_id].update(dp.chat_data.get(old_id))
        del dp.chat_data[old_id]

...

def main():
    updater = Updater("TOKEN", use_context=True)
    dp = updater.dispatcher # available since version 12.4

    dp.add_handler(MessageHandler(Filters.status_update.migrate, chat_migration))

...
```
To be entirely sure that the update will be processed by this handler, either add it first or put it in its own group.

### ChatMigrated Errors

If you try e.g. sending a message to the old chat id, Telegram will respond by a Bad Request including the new chat id. You can access it using an error handler:

```python
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

    if isinstance(context.error, ChatMigrated):
        new_chat_id = context.error.new_chat_id
```
Unfortunately, Telegram does *not* pass along the old chat id, so there is currently no simple way to perform a data transfer like above within the error handler. So make sure, that you catch the status updates! Still, you can wrap your requests into a `try-except`-clause:

```python
def my_callback(update, context):
    dp = context.dispatcher # available since version 12.4

    ...

    try:
        context.bot.send_message(chat_id, text)
    except ChatMigrated as e:
        new_id = e.new_chat_id

        # Resend to new chat id
        context.bot.send_message(new_id, text)

        # Transfer data
        if chat_id in dp.chat_data:
            dp.chat_data[new_id].update(dp.chat_data.get(chat_id))
            del dp.chat_data[chat_id]

    ...
```
