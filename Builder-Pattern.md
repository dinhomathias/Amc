# The Builder Pattern in `telegram.ext`

In this library, there are roughly four different components that make up everything:

1. The `Updater` is responsible for fetching updates that Telegram sent to your bot
2. The `Dispatcher` is responsible for handling those updates by passing them to the different handlers
3. The `Bot` provides high-level access to the methods of the Bot API
4. The `BaseRequest` is responsible to handle the actual networking stuff, i.e. sending the requests to the Bot API

All of those have different parameters. Some of them are optional. Some are required. Some are mutually exclusive.
That's a lot to take in and when coding your bot, setting this all up by yourself would be tiresome.

That's why `python-telegram-bot` makes an effort to make the setup easy with reasonable defaults. E.g. with

```python
from telegram.ext import Updater
updater = Updater.builder().token('TOKEN').build()
```

`python-telegram-bot` you will automatically have

* the `Dispatcher` available as `updater.dispatcher`
* the `Bot` available as `updater/dispatcher.bot`
* the `BaseRequest` available as `updater/dispatcher.bot.request`

So what if you want to customize some attributes that `Updater`, `Dispatcher`, `Bot` or `BaseRequest` accept? Do you have to build all those objects yourself and glue them together? No! Well, you can, but you don't have to.

This is, where the [builder patter](https://en.wikipedia.org/wiki/Builder_pattern) comes into play. The idea is roughly as follows: You went shopping and have all the ingredients for a nice stew, but you don't want to cook yourself. So you hand everything to a chef. The chef will tell you that some of your ingredients don't match and will discard them. But then, he'll cook a nice stew for you and you never need to worry about how exactly that's done.

Let's get a bit more technical. First, we need the cook:

```python
from telegram.ext import Updater
builder = Updater.builder()
```

Now, we hand over the ingredients:

```python
builder.token(token)  # the bot token is the main ingredient
builder.context_types(context_types)  # In case you want to use custom context types for your `Dispatcher`
builder.request_kwargs(request_kwargs)  # In case you want to fine tune the networking backend
...
```

Finally, we have the chef cook the stew:

```python
updater = builder.build()
```

All this can also be chained into a single line:


```python
from telegram.ext import Updater
updater = Updater.builder().token(token).context_types(context_types).request_kwargs(request_kwargs).build()
```

And that's already it! A similar pattern can also be used in case you just need the `Dispatcher` (e.g. if you have a custom webhook setup and don't need the `Updater`). In that case, you'll just do something like

```python
from telegram.ext import Dispatcher
dispatcher = Dispatcher.builder().token(token)….build()
```

The docs of [`UpdaterBuilder`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.updaterbuilder.html) and [`DispatcherBuilder`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.dispatcherbuilder.html) have all the info about which "ingredients" they can handle, i.e. which methods they have. Each method will tell you

* how the parameters will be used (e.g. the token passed to `UpdaterBuilder.token` will be used for the `Bot` available as `Updater.bot`)
* What happens if you don't call this method. For many things, PTB will use reasonable defaults.
