## Introduction
The `telegram.ext` submodule is built on top of the pure API implementation. It provides an easy-to-use interface and takes some work off the programmer, so you [don't have to repeat yourself](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)

It consists of several classes, but the two most important ones are `telegram.ext.Updater` and `telegram.ext.Dispatcher`.

The `Updater` class continuously fetches new updates from telegram and forwards them to the `Dispatcher` class. 
If you create an `Updater` object, it will create a `Dispatcher` for you and link them together with a `Queue`. 
You can then register handlers of different types in the `Dispatcher`, which will sort the updates fetched by the `Updater` according to the handlers you registered, and deliver them to a callback function that you defined.

Every handler is an instance of any subclass of the `telegram.ext.Handler` class. The library provides handler classes for almost all your needs, but if you need something very specific, you can also subclass `Handler` yourself.

To begin, you'll need an Access Token. If you already read and followed [Introduction to the API](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API), you can use the one you generated then. If not: To generate an Access Token, you have to talk to [@BotFather](https://telegram.me/botfather) and follow a few simple steps (described [here](https://core.telegram.org/bots#botfather)). You should really read the introduction first, though.


## Your first Bot, step-by-step
So, *let's get started!* Again, please fire up a Python command line if you want to follow this tutorial.

First, you have to create an `Updater` object. Replace `'TOKEN'` with your Bot's API token.

```python
>>> from telegram.ext import Updater
>>> updater = Updater(token='TOKEN')
```
**Related docs:** [telegram.ext.Updater](http://pythonhosted.org/python-telegram-bot/telegram.ext.updater.html#telegram.ext.updater.Updater)

For quicker access to the `Dispatcher` used by your `Updater`, you can introduce it locally:

```python
>>> dispatcher = updater.dispatcher
```

Now, you can define a function that should process a specific type of update:

```python
>>> def start(bot, update):
...     bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
```
**Related docs:** [sendMessage](https://core.telegram.org/bots/api#sendmessage)

The goal is to have this function called every time the Bot receives a Telegram message that contains the `/start` command. To accomplish that, you can use a `CommandHandler` (one of the provided `Handler` subclasses) and register it in the dispatcher:

```python
>>> from telegram.ext import CommandHandler
>>> start_handler = CommandHandler('start', start)
>>> dispatcher.add_handler(start_handler)
```
**Related docs:** [telegram.ext.CommandHandler](http://pythonhosted.org/python-telegram-bot/telegram.ext.commandhandler.html), [telegram.ext.Dispatcher.add_handler](http://pythonhosted.org/python-telegram-bot/telegram.ext.dispatcher.html#telegram.ext.dispatcher.Dispatcher.add_handler)

And that's all you need. To start the bot, run:

```python
>>> updater.start_polling()
```
**Related docs:** [telegram.ext.Updater.start_polling](http://pythonhosted.org/python-telegram-bot/telegram.ext.updater.html#telegram.ext.updater.Updater.start_polling)

Give it a try! Start a chat with your bot and issue the `/start` command - if all went right, it will reply.

But the Bot not doing anything yet, besides answering to the `/start` command. Let's add another handler that listens for regular messages. Use the `MessageHandler`, another `Handler` subclass, to echo to all text messages:

```python
>>> def echo(bot, update):
...     bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)
...
>>> from telegram.ext import MessageHandler, Filters
>>> echo_handler = MessageHandler([Filters.text], echo)
>>> dispatcher.add_handler(echo_handler)
```
**Related docs:** [telegram.ext.MessageHandler](http://pythonhosted.org/python-telegram-bot/telegram.ext.messagehandler.html)

From now on, your bot should reply to all regular text messages that don't start with a command with a message that has the same content.

**Note:** As soon as you add new handlers to `dispatcher`, they are in effect.

**Note:** The `Filters` class contains a number of functions that filter incoming messages for text, images, status updates and more. Any message that returns `True` for at least one of the filters passed to `MessageHandler` will be accepted. You can also use your own filtering functions if you want - it should take a single parameter of type `telegram.Message`.

Let's add some actual functionality to your bot. We want to implement a `/caps` command that will take some text as an argument and reply to it in CAPS. To make things easy, you can receive the arguments (as a `list`, split on spaces) that were passed to a command in the callback function:

```python
>>> def caps(bot, update, args):
...     text_caps = ' '.join(args).upper()
...     bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)
...
>>> caps_handler = CommandHandler('caps', caps, pass_args=True)
>>> dispatcher.add_handler(caps_handler)
```

**Note:** Take a look at the `pass_args=True` in the `CommandHandler` initiation. This is required to let the handler know that you want it to pass the list of command arguments to the callback. All handler classes have keyword arguments like this. Some are the same among all handlers, some are specific to the handler class. If you use a new type of handler for the first time, look it up in the docs and see if one of them is useful to you.

Another cool thing in the Telegram Bot API is the [inline mode](https://core.telegram.org/bots/inline). If you want to implement inline functionality for your bot, please first talk to [@BotFather](https://telegram.me/botfather) and enable inline mode using `/setinline`. It sometimes takes a while until your Bot registers as an inline bot on your client. You might be able to speed up the process by restarting your Telegram App (or sometimes, you just have to wait for a while).

As your bot is obviously a very loud one, let's continue with this theme for inline. You probably know the process by now, but there are a number of new types used here, so pay some attention:

```python
>>> from telegram import InlineQueryResultArticle, InputTextMessageContent
>>> def inline_caps(bot, update):
...     query = bot.update.inline_query.query
...     if not query:
...         return
...     results = list()
...     results.append(
...         InlineQueryResultArticle(
...             id=query.upper(),
...             title='Caps',
...             input_message_content=InputTextMessageContent(query.upper())
...         )
...     )
...     bot.answerInlineQuery(update.inline_query.id, results)
...
>>> from telegram.ext import InlineQueryHandler
>>> inline_caps_handler = InlineQueryHandler(inline_caps)
>>> dispatcher.add_handler(inline_caps_handler)
```
**Related docs:** [telegram.ext.InlineQueryHandler](http://pythonhosted.org/python-telegram-bot/telegram.ext.inlinequeryhandler.html), [answerInlineQuery](https://core.telegram.org/bots/api#answerinlinequery)

Not bad - Your Bot can now yell on command (ha!) and via inline. 

Some confused users might try to send commands to the bot that it doesn't understand, so you can use a `MessageHandler` with a `command` filter to reply to all commands that were not recognized by the previous handlers. 

```python
>>> def unknown(bot, update):
...   bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
...
>>> unknown_handler = MessageHandler([Filters.command], unknown)
>>> dispatcher.add_handler(unknown_handler)
```

**Note:** This handler *must* be added last. If you added it sooner, it would be triggered before the `CommandHandlers` had a chance to look at the update. Once an update is handled, all further handlers are ignored. To circumvent this, you can pass the keyword argument `group (int)` to `add_handler` with a value other than 0.

If you're done playing around, stop the bot with this:

```python
>>> updater.stop()
```

**Note:** As you have read earlier, the `Updater` runs in a seperate thread. That is very nice for this tutorial, but if you are writing a script, you probably want to stop the Bot by pressing Ctrl+C or sending a signal to the Bot process. To do that, use `updater.idle()`. It blocks execution until one of those two things occur, then calls `updater.stop()` and then continues execution of the script.

#### What to read next?
Learn about the library exceptions and best practices in [Exception Handling](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Exception-Handling)

You want *moar features*? Check out [Extensions – JobQueue](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue)!

Check out more examples in the [examples folder](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples)!