# Flood Limits & Why to Avoid Them

Considering [Telegram's Bot documentation](https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this), currently the maximum amount of messages being sent by bots is limited to ~30 messages/second for all ordinary messages and ~20 messages/minute for group messages.
According to [@BotSupport](https://t.me/BotSupport) the limit for group also applies to channels (this is not confirmed by Telegram in their documentation however).
We emphasize that Telegram does *not* document the precise limits, neither for sending messages nor for other kinds of API requests.
Moreover, the limits may differ between bots and also over time. 

When your bot hits spam limits, it starts to get `RetryAfter` errors from Telegram API.
If you want to make sure that the message is actually sent and hence just try again on every `RetryAfter` error, your code would spend a significant amount resources just on those retries.
Moreover, constantly retrying to send messages while ignoring API errors could result in your bot being banned for some time.

That means, if you're making a production-ready bot that is expected to have a large number of users, it's a good idea to use throughput limiting mechanism for messages being sent/requests being made to the Bot API.
This way you can ensure that all messages would be delivered to end-users as soon as possible in ordered way.

# PTBs Rate Limiting Mechanism

Since v20 (v20.0a3, to be precise), PTB comes with a built-in mechanism to throttle the number of API requests that your bot makes per time interval.
This mechanism is exposed through the `telegram.ext.BaseRateLimiter` interface class.
This class has basically one important abstract coroutine method, called `BaseRateLimiter.process_request`.
This method is called every time when your bot makes an API request and it's purpose is to delay the request such that your bot doesn't hit the rate limits.
Any implementation of `BaseRateLimiter` can implement its own logic on how this should be done.
If you observe a particular pattern in how your bot receives `RetryAfter` errors (e.g. messages to one particular group trigger `RetryAfter` errors quickly), you can implement a logic that addresses these specific patterns.

The `BaseRateLimiter` setup can be used only with `telegram.ext.ExtBot`, not with `telegram.Bot`.
It's easy to set up and use.
Assume that `MyLimiter` implements `BaseRateLimiter`.
Then we use like this:

```python
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

application = ApplicationBuilder().token("TOKEN").rate_limiter(MyLimiter()).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This is automatically passed through `MyLimiter.process_request`!
    await update.message.reply_text(text="Hello World!")


application.add_handler(CommandHandler('start', start))
```

You may also pass additional information to `MyLimiter.process_request`.
Imagine that you want to broadcast a message to all the users of your bot.
You might want to give those messages a lower priority, answering requests of your users should be faster.
This could look like this:

```python
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

application = ApplicationBuilder().token("TOKEN").rate_limiter(MyLimiter()).build()
user_ids = [1, 2, 3]

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(text="Starting the broadcast...")
    context.application.create_task(
        asyncio.gather(
            *(
                context.bot.send_message(
                    chat_id=user_id, text="Hello World!", rate_limit_args={'priority': -1}
                )
                for user_id in user_ids
            )
        )
    )


application.add_handler(CommandHandler('broadcast', broadcast))
```

What kind of input is allowed for the `rate_limit_args` argument is up to the implementation of `BaseRateLimiter`.

# Built-in Rate Limiter

PTB comes with a built-in implementation of `BaseRatelimiter`: The class `telegram.ext.AIORateLimiter` uses the library [aiolimiter](https://aiolimiter.readthedocs.io/).
Please consult the documentation of `AIORateLimiter` for details on how it applies rate limits to API requests and how it should be used.

⚠️  We emphasize that `AIORateLimiter` is to be understood as minimal effort reference implementation.
If you would like to handle rate limiting in a more sophisticated, fine-tuned way, we
welcome you to implement your own subclass of `telegram.ext.BaseRateLimiter`.
Feel free to check out the [source code of `AIORateLimiter`](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/telegram/ext/_aioratelimiter.py#L51) class for inspiration.

