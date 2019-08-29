## Table of contents
* [Context based callbacks](#context-based-callbacks)
    * [What exactly is CallbackContext](#what-exactly-is-callbackcontext)
    * [Handler callbacks](#handler-callbacks)
    * [Error handler callbacks](#error-handler-callbacks)
    * [Job callbacks](#job-callbacks)
    * [Note about group and groupdict](#note-about-group-and-groupdict)
    * [Note about version 13](#note-about-version-13)
    * [Custom handlers](#custom-handlers)
* [Handler changes](#handler-changes)
    * [CommandHandler](#commandhandler)
    * [PrefixHandler](#prefixhandler)
    * [MessageHandler](#messagehandler)
    * [ConversationHandler](#conversationhandler)
    * [Error Handler](#error-handler)
* [Filters in handlers](#filters-in-handlers)
    * [Special note about regex filters](#special-note-about-regex-filters)
* [Persistence](#persistence)
* [Return UTC from from_timestamp()](#return-utc-from-from_timestamp)

# Context based callbacks
The biggest change in this release is context based callbacks. When running your bot you will probably see a warning like the following:
```
echobot2.py:62: TelegramDeprecationWarning: Old Handler API is deprecated - see https://git.io/vp113 for details
```
This means you're using the old style callbacks and should upgrade to context based callbacks.

The first thing you should do is find where you create your `Updater`.
``` python
updater = Updater('TOKEN')
```
And add `use_context=True` so it looks like
```python
updater = Updater('TOKEN', use_context=True)
```
**Note that this is only necessary in version 12 of `python-telegram-bot`. Version 13 will have `use_context=True` set as default.**  
_If you do **not** use `Updater` but only `Dispatcher` you should instead set `use_context=True` when you create the `Dispatcher`._

## What exactly is `CallbackContext`
[`CallbackContext`](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.callbackcontext.html) is an object that contains all the extra context information regarding an `Update`, error or `Job`. It replaces the old behaviour with having a ton of `pass_something=True` in your handlers. Instead, all this data is available directly on the `CallbackContext` - always!
So what information is stored on a `CallbackContext`? The parameters marked with a star will only be set on specific updates.
* bot
* job_queue
* update_queue
* chat_data*
* user_data*
* job*
* error*
* args*
* matches/match*

## Handler callbacks
Now on to the bulk of the change. You wanna change all your callback functions from the following:
``` python
def start(bot, update, args, job_queue):
    # Stuff here
```

to the new style using CallbackContext
``` python
def start(update: Update, context: CallbackContext):
    # Stuff here
    # args will be available as context.args
    # jobqueue will be available as context.jobqueue
```
_On python 2 which doesn't support annotations replace `update: Update, context: CallbackContext` with simply `update, context`._

## Error handler callbacks
Error handler callbacks are the ones added using `Dispatcher.add_error_handler`. These have also been changed from the old form:
```python
def error_callback(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
```
into
```python
def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)
```
_Note that the error is now part of the `CallbackContext` object._

## Job callbacks
Job callbacks (the ones that are passed to `JobQueue.run_once` and similar) have also changed. Old form:
``` python
def job_callback(bot, job):
   bot.send_message(SOMEONE, job.context)
```
New form:
``` python
def job_callback(context):
    job = context.job
    context.bot.send_message(SOMEONE, job.context)
```
_Note that both bot, and job have been merged into the `CallbackContext` object._

## Note about groups and groupdict
Before version 12, you could both pass_groups and pass_groupdict. Inside `CallbackContext` this has been combined into a single `Match` object. Therefore if your handler looked like this before:
``` python
def like_callback(bot, update, groups, groupdict): # Registered with a RegexHandler with pattern (?i)i (like|dislike) (?P<thing>.*)
    update.reply_text('You {} {}'.format(groups[1], groupdict['thing'])
```
It would instead now look something like this:
``` python
def like_callback(update, context): # Registered with a RegexHandler with pattern (?i)i (like|dislike) (?P<thing>.*)
    update.reply_text('You {} {}'.format(context.match[1], context.match.groupdict()['thing'])
```
Also see [Special note about regex filters](#special-note-about-regex-filters).

## Note about version 13
In version 13 of `python-telegram-bot`, `use_context` will default to `True`. This means that your old handlers using pass_ will stop working. It also means that after upgrading to version 13, you can remove `use_context=True` from your `Updater` if you so desire.

# Custom handlers
This part is only relevant if you've developed custom handlers, that subclass `telegram.ext.Handler`. To support the new context based callbacks, add a method called `collect_additional_context` to your handler. The method receives a `CallbackContext` object and whatever is return by `check_update()`, and should add whatever extra context is needed (at least everything that could be added via `pass_` arguments before). Note that `job_queue, update_queue, chat_data, user_data` is automatically added by the base `Handler`.

***
# Handler changes
We made some changes to the behaviour of some handlers. Listed below are the changes notable to you and maybe requires some action in your code.

## CommandHandler
From now on `CommandHandler` will only respond to [valid bot commands](https://core.telegram.org/bots#commands). It will raise `ValueError` when an invalid command is given as the `command` argument. If you previously used commands not considered valid by @botfather, you can use the new [PrefixHandler](#prefixhandler) instead.
In addition `allow_edited` is deprecated until V13, when it will be removed. The new default behavior is to accept both `message` and `edited_message` with a valid command. If you would like to exclude edited message from your CommandHandler pass `filters=~Filters.update.edited_message` to the constructor.

## PrefixHandler
Newly added is the `PrefixHandler`. [read the docs ](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.prefixhandler.html) for more details on its use and implementation.

## MessageHandler
`MessageHandler` received some upgrades to switch to the filter system. We've removed `allow_edited` which has been deprecated for a while. Also we now deprecated `message_updates`, `channel_post_updates` and `edited_updates` in the constructor. The defaults remain the same (not edited messages and channel_posts). To tweak the message you receive with MessageHandler, please use the [update filters](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.filters.html#telegram.ext.filters.Filters.update).

## RegexHandler
`RegexHandler` is being deprecated. It's basically a MessageHandler with a `Filters.regex`, now the CallbackContext contains all match information. For now, we keep it in, but you should switch the use of `RegexHandler` to using `MessageHandler(Filters.regex('pattern'), callback)`.  
See [Special note about regex filters](#special-note-about-regex-filters) and [Note about group and groupdict](#note-about-group-and-groupdict) for more details.

## ConversationHandler
The arguments `run_async_timeout` and `timed_out_behavior` have been removed.
The timeout for waiting for a @run_async handler is now always 0. If an update would have waited before, ConversationHandler will now try to use a handler in the new special state `ConversationHandler.WAITING`. This allows you to either manually wait in the handler if you want the old functionality, or send a message back to the user like "I am still processing your last request, please wait".

## Error handler
Error handler got a major improvement. Instead of only handling TelegramErrors, every error from every handler will be passed to its callback.

You can use it for example to send yourself notifications if an error happened while your bot is running.

Note: If an error handler callback is successfully executed, the error itself won't be caught by the logger module. If you still want this, reraise the error at the end of your function.

***
# Filters in handlers
Using a list of filters in a handler like below has been deprecated for a while now. Version 12 removes the ability completely.
``` python
MessageHandler([Filters.audio, Filters.video], your_callback)
```
## Combine filters using bitwise operators
Instead, you can now combine filters using bitwise operators like below. (The pipe ( `|` ) character means OR, so the below is equivalent to the above example using a list).
``` python
# Handle messages that contain EITHER audio or video
MessageHandler(Filters.audio | Filters.video, your_callback)
```
### Also supports AND, NOT and more than 3 filters
**AND:**
```python
# Handle messages that are text AND contain a mention
Filters.text & Filters.entity(MesageEntity.MENTION)
```
**NOT:**
``` python
# Handle messages that are NOT commands (same as Filters.text in most cases)
~ Filters.command
```
**More advanced combinations:**
``` python
# Handle messages that are text and contain a link of some kind
Filters.text & (Filters.entity(URL) | Filters.entity(TEXT_LINK))
# Handle messages that are text but are not forwarded
Filters.text & (~ Filters.forwarded)
```

### Special note about regex filters
Regex filters can also be used in advanced combinations like so:  
``` python
((Filters.regex('(test)') | Filters.command) & (Filters.regex('(it)') | Filters.forwarded))
```
This would make `context.matches` equal a list of regex matches, but only if the regex filter actually executed. This means that:
 * it will be a list with a single match for `test` if it's a command but not forwarded.
 * it will be a list with a single match for `it` if it's forwarded but not a command.
 * it will be a list of two matches. The first one will be `test` and the second one `it`.
Note that in the last case, the order is the order that the filters were executed in, and not necessarily left to right.

Also note that `context.match` is a shortcut for `context.matches[0]`. Very useful when you are only interested in the first match.

***
# Persistence
In version 12 we introduce persistence to the bot's mechanics. If you want to use this please read the [wiki page](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent) dedicated to persistence.
***
# Return UTC from from_timestamp()

from_timestamp() now returns UTC timestamps. The recommended way to work is to run your bot on a machine configured to UTC.