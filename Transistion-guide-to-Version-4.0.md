# What's new?

## Dispatcher

The `Dispatcher` class has now a cleaner interface and more precise Message filtering. Instead of many methods with long names like `Dispatcher.addTelegramMessageHandler(handler)`, we now only have two of those methods:

> #### addHandler(handler, group=0)
> Register a handler. A handler must be an instance of a subclass of `telegram.ext.Handler`. All handlers are organized in groups, the default group is `int(0)`, but any object can identify a group. Every update will be tested against each handler in each group from first-added to last-added. If the update has been handled in one group, it will not be tested against other handlers in that group. That means an update can only be handled 0 or 1 times per group, but multiple times across all groups.

> ##### Parameters:
> `handler (Handler)` – A Handler instance  
> `group (optional[object])` – The group identifier. Default is 0

> #### addErrorHandler(callback)   

> This method remains unchanged.

So, the `addHandler` method is accepting an object of a subclass of `telegram.ext.Handler`. Let's see how that looks in real life:

```
from telegram.ext import MessageHandler, filters

def text_callback(bot, update):
  print("New text message: " + update.message.text)

dispatcher.addHandler(MessageHandler([filters.TEXT], text_callback))
```

As you can see here, the `MessageHandler` class is one of the included `Handler` subclasses. All that was possible before is still possible, but now more organized and more explicit. Lets take a quick look at another handler class, the `RegexHandler`:

```
from telegram.ext import RegexHandler

def name_callback(bot, update, groupdict):
  print("The name of the user is: " + groupdict['name'])

name_regex = r'My name is (?P<name>.*)'
dispatcher.addHandler(RegexHandler(name_regex, text_callback, pass_groupdict=True))
```
Here you can see the optional argument `groupdict` passed to the handler callback function. Note that it is necessary to specify this explicitly when creating the `Handler` object.

### Other changes
* You can easily implement your own handlers. Just subclass `telegram.ext.handler` and take a look at the implementation of the provided handlers.
* Instead of `addTelegramInlineHandler` there are now `InlineHandler`, `ChosenInlineResultHandler` and `CallbackQueryHandler`
* There is no replacement for `addUnknownTelegramCommandHandler`. Instead, it is recommended to use `RegexHandler(r'/.*', ...) and add it as the last handler
* The `UpdateQueue` class and `context` parameters have been removed
## Bot API 2.0