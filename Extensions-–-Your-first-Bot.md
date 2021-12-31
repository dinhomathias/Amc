## Introduction
The `telegram.ext` submodule is built on top of the pure API implementation. It provides an easy-to-use interface and takes some work off the programmer, so you [don't have to repeat yourself](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself).

It consists of several classes, but the two most important ones are [`telegram.ext.Updater`](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.updater.html#telegram.ext.Updater) and [`telegram.ext.Dispatcher`](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.dispatcher.html#telegram.ext.Dispatcher).

The `Updater` class continuously fetches new updates from telegram and passes them on to the `Dispatcher` class. 
If you create an `Updater` object, it will create a `Dispatcher` for you and link them together with a `Queue`. 
You can then register handlers of different types in the `Dispatcher`, which will sort the updates fetched by the `Updater` according to the handlers you registered, and deliver them to a callback function that you defined.

Every handler is an instance of any subclass of the [`telegram.ext.Handler`](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.handler.html#telegram.ext.Handler) class. The library provides [[handler classes for almost all use cases|Types-of-Handlers]], but if you need something very specific, you can also subclass `Handler` yourself.

To begin, you'll need an Access Token. If you have already read and followed [[Introduction to the API|Introduction-to-the-API]], you can use the one you generated then. If not: To generate an Access Token, you have to talk to [@BotFather](https://telegram.me/botfather) and follow a few simple steps (described [here](https://core.telegram.org/bots#6-botfather)). You should really read the introduction first, though.


## Your first Bot, step-by-step
So, *let's get started!* Again, please fire up a Python command line if you want to follow this tutorial.

First, you have to create an `Updater` object. Replace `'TOKEN'` with your Bot's API token.

```python
from telegram.ext import Updater
updater = Updater(token='TOKEN', use_context=True)
```
**Related docs:** [`telegram.ext.Updater`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.updater.html#telegram.ext.updater.Updater)

**Note**: The `use_context=True` is a special argument only needed for version 12 of the library. The default value is `False`. It allows for better backwards compatibility with older versions of the library, and to give users some time to upgrade. From version 13 `use_context=True` it is the default.

For quicker access to the `Dispatcher` used by your `Updater`, you can introduce it locally:

```python
dispatcher = updater.dispatcher
```

This is a good time to set up the `logging` module, so you will know when (and why) things don't work as expected:

```python
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
```

**Note:** Read the article on [[Exceptions, Warnings and Logging|Exceptions,-Warnings-and-Logging]] if you want to learn more.

Now, you can define a function that should process a specific type of update:

```python
from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
```
**Related docs:** [`send_message`](https://core.telegram.org/bots/api#sendmessage), [`telegram.ext.CallbackContext` (the type of the context argument)](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.callbackcontext.html), [`telegram.Update` (the type of update argument)](https://python-telegram-bot.readthedocs.io/en/latest/telegram.update.html)

The goal is to have this function called every time the Bot receives a Telegram message that contains the `/start` command. To accomplish that, you can use a `CommandHandler` (one of the provided `Handler` subclasses) and register it in the dispatcher:

```python
from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
```
**Related docs:** [`telegram.ext.CommandHandler`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.commandhandler.html), [`telegram.ext.Dispatcher.add_handler`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.dispatcher.html#telegram.ext.dispatcher.Dispatcher.add_handler)

And that's all you need. To start the bot, run:

```python
updater.start_polling()
```
**Related docs:** [`telegram.ext.Updater.start_polling`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.updater.html#telegram.ext.updater.Updater.start_polling)

Give it a try! Start a chat with your bot and issue the `/start` command - if all went right, it will reply.

But our Bot can now only answer to the `/start` command. Let's add another handler that listens for regular messages. Use the `MessageHandler`, another `Handler` subclass, to echo all text messages:

```python
from telegram.ext import MessageHandler, Filters

def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)
```
**Related docs:** [`telegram.ext.MessageHandler`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.messagehandler.html), [`telegram.ext.filters`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.filters.html)

From now on, your bot should echo all non-command messages it receives.

**Note:** As soon as you add new handlers to `dispatcher`, they are in effect.

**Note:** The `Filters` class contains a number of so called filters that filter incoming messages for text, images, status updates and more. Any message that returns `True` for at least one of the filters passed to `MessageHandler` will be accepted. You can also write your own filters if you want. See more in [[Advanced Filters|Extensions-–-Advanced-Filters]].

Let's add some actual functionality to your bot. We want to implement a `/caps` command that will take some text as an argument and reply to it in CAPS. To make things easy, you can receive the arguments (as a `list`, split on spaces) that were passed to a command in the callback function:

```python
def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)
```

**Note:** Take a look at the usage of `context.args`. The [`CallbackContext`](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.callbackcontext.html) will have many different attributes, depending on which handler is used.

Another cool feature of the Telegram Bot API is the [inline mode](https://core.telegram.org/bots/inline). If you want to implement inline functionality for your bot, please first talk to [@BotFather](https://telegram.me/botfather) and enable inline mode using `/setinline`. It sometimes takes a while until your Bot registers as an inline bot on your client. You might be able to speed up the process by restarting your Telegram App (or sometimes, you just have to wait for a while).

As your bot is obviously a very loud one, let's continue with this theme for inline. You probably know the process by now, but there are a number of new types used here, so pay some attention:

```python
from telegram import InlineQueryResultArticle, InputTextMessageContent
def inline_caps(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

from telegram.ext import InlineQueryHandler
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)
```
**Related docs:** [telegram.ext.InlineQueryHandler](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.inlinequeryhandler.html), [answerInlineQuery](https://core.telegram.org/bots/api#answerinlinequery)

Not bad! Your Bot can now yell on command (ha!) and via inline mode. 

Some confused users might try to send commands to the bot that it doesn't understand, so you can use a `MessageHandler` with a `command` filter to reply to all commands that were not recognized by the previous handlers. 

```python
def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
```

**Note:** This handler *must* be added last. If you added it sooner, it would be triggered before the `CommandHandlers` had a chance to look at the update. Once an update is handled, all further handlers are ignored. To circumvent this, you can pass the keyword argument `group (int)` to `add_handler` with a value other than 0. See [`telegram.ext.Dispatcher.add_handler`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.dispatcher.html#telegram.ext.dispatcher.Dispatcher.add_handler) for details.

If you're done playing around, stop the bot with:

```python
updater.stop()
```

**Note:** As you have read earlier, the `Updater` runs in a separate thread. That is very nice for this tutorial, but if you are writing a script, you probably want to stop the Bot by pressing Ctrl+C or sending a signal to the Bot process. To do that, use `updater.idle()`. It blocks execution until one of those two things occur, then calls `updater.stop()` and then continues execution of the script.

#### What to read next?
Have a look at the ready-to-run [examples](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples).

Learn about the library exceptions and best practices in [[Exceptions, Warnings and Logging|Exceptions,-Warnings-and-Logging]].

You want *more features*? Check out [[Extensions – JobQueue|Extensions-–-JobQueue]]!