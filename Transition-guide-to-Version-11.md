## Table of contents
* [Context based handlers](#context-based-handlers)
* [Filters in handlers](#filters-in-handlers)

# Context based handlers
The biggest change in this release is context based handlers. When running your bot you will probably see a warning like the following:
```
echobot2.py:62: TelegramDeprecationWarning: Old Handler API is deprecated - see https://git.io/vpVe8 for details
  dp.add_handler(CommandHandler("help", help))
```
This is telling you to change all your handlers and handler callbacks from the old style
``` python
def start(bot, update, args, job_queue):
    # Stuff here

# Later
dp.add_handler(CommandHandler("help", help., pass_jobqueue=True, pass_args=True))
```

to the new style using HandlerContext
``` python
def start(update: Update, context, HandlerContext):
    # Stuff here
    # args will be available as context.args
    # jobqueue will be available as context.jobqueue

# Later
dp.add_handler(CommandHandler("help", help, use_context=True))
```
or on _python 2_ which doesn't support annotations replace `update: Update, context, HandlerContext` with simply `update, context`.

## What exactly is `HandlerContext`
`HandlerContext` is an object that contains all the extra context information regarding an update. It replaces the old behaviour with having a ton of `pass_something=True` in your handlers. Instead, all this data is availible directly on the `HandlerContext` - always!

## Note about groups and groupdict
Before version 11, you could both pass_groups and pass_groupdict. Inside `HandlerContext` this has been combined into a single `Match` object. Therefore if your handler looked like this before:
``` python
def like_callback(bot, update, groups, groupdict):
    update.reply_text('You {} {}'.format(groups[1], groupdict['thing'])

dp.add_handler(RegexHandler(r'(?i)i (like|dislike) (?P<thing>.*)', like_callback, pass_groups=True, pass_groupdict=True))
```
It would instead now look something like this:
``` python
def like_callback(update, context):
    update.reply_text('You {} {}'.format(context.match[1], context.match.groupdict()['thing'])

dp.add_handler(RegexHandler(r'(?i)i (like|dislike) (?P<thing>.*)', like_callback, use_context=True))
```

## About version 12
In version 12 of python-telegram-bot, `use_context` will default to `True`. This means that your old handlers using pass_ will stop working. It also means that after upgrading to version 12, you can remove `use_context=True` from your handlers if you so desire.

## Just disabling the warning
You can also simply disabling the warning, if you're planing on migrating to context based handlers in the future. THIS IS NOT RECOMMENDED. In version 12 your bot WILL STOP WORKING if you do not switch to context based handlers.

```python
import warnings
from telegram.utils.deprecate import TelegramDeprecationWarning
warnings.filterwarnings('ignore', category=TelegramDeprecationWarning)
```


***

# Filters in handlers
Using a list of filters in a handler like below has been deprecated for a while now. Version 11 removes the ability completely.
``` python
MessageHandler([Filters.audio, Filters.video], your_callback)
```
## Combine filters using bitwise operators
Instead you can now combine filters using bitwise operators like below. (The pipe ( `|` ) character means OR, so the below is equalivant to the above example using a list).
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
