## What the spam limits are and why you should avoid hitting them
Considering [Telegram's Bot documentation](https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this), currently the maximum amount of messages being sent by bots is limited to 30&#160;messages/second for all ordinary messages and 20&#160;messages/minute for group messages. When your bot hits spam limits, it starts to get 429 errors from Telegram API. And assuming that error handling in such case usually is coded as simple retrials, the running machine would spend a lot of CPU time retrying (or got locked down, depending on bot implementation details). And constantly retrying to send messages while ignoring API errors could result in your bot being banned for some time.

That means, if you're making a production-ready bot, which should serve numerous users **it's always a good idea to use throughput limiting mechanism for messages being sent**. This way you could be sure that all messages would be delivered to end-users as soon as possible in ordered way.

## Available tools and their implementation details
The previously described throughput-limiting mechanism is provided in the `telegram.ext.messagequeue` submodule. It contains a [`MessageQueue`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.messagequeue.html) main class which passes sendmessage callbacks through one or two delay queues (instances of [`DelayQueue`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.delayqueue.html) class) depending on message type (ordinary or group message). The figure below illustrates how it works: 

![flow chart](https://cloud.githubusercontent.com/assets/16870636/23493181/82244f60-ff12-11e6-8fd7-679fdbd16b04.png)

Each [`DelayQueue`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.delayqueue.html) instance runs in a separate thread waiting for new callbacks to appear on internal python's `queue.Queue` and calculating the required delays before running these callbacks according to time-window scheme. For providing delays, it relies on `time.sleep` and on `threading.Queue` locking when there are no new callbacks to dispatch, therefore it's a ridiculously CPU-efficient implementation.
However, you should be aware that **callbacks always run in non-main (DelayQueue) thread**. That's not a problem for Python-Telegram-Bot lib itself, but in rare cases you may still need to provide additional locking etc to thread-shared resources. So, just keep that fact in mind.

The described time-window delay calculation scheme has many similarities with windowing in DSP theory and is better illustrated on the figure below.

![windowing](https://user-images.githubusercontent.com/16870636/28248541-e7cfca4a-6a4e-11e7-84e8-ad1992e21fd4.png)

Internally, [`DelayQueue`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.delayqueue.html) performs windowing by keeping track of messages being sent times in a list (at most M-sized), dynamically shrinking and expanding it as needed which is a very robust solution. The throughput limit at M&#160;messages/N&#160;milliseconds is set as M `burst_limit` and N `time_limit_ms` arguments. However, be aware that 30&#160;messages/1&#160;second is not the same as 60&#160;messages/2&#160;seconds as the latter would allow sends of 60 messages in a small-time bulk (in this case, should be smaller than 2 seconds), which could quickly lead you directly into banlist. As a result, **you should never specify `burst_limit` higher than 30 messages** (and 20 for group-type message delay).

To compare apples to apples, send times are calculated on the bot side, but the actual spam limiting occurs on Telegram's side. There are numerous additional delays, jitter and buffering effects happening: on the OS networking scheduler, global Internet networking hardware, on the Telegram's servers processing API requests etc. If you're not willing to push all the jam out of Telegram's spam control, **we'd recommend specifying stricter [`MessageQueue`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.messagequeue.html) limits than Telegram currently has.** Ordinary message throughput limit at 29&#160;messages/1017&#160;milliseconds would work like a charm and give you the 5% safety margin.

Each message being sent is encapsulated in a callback to the corresponding send method. The [`DelayQueue`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.delayqueue.html) class could process any callables with delays, not only encapsulated send callbacks, so it's generic and broadly useful even outside of it's current scope. We use and recommend using [`telegram.utils.promise.Promise`](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/telegram/utils/promise.py#L29) for that as it allows the delayed exception handling and has a convenient interface.

If you need more details on MQ implementation, [follow its docs](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.messagequeue.html) or [read the source](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/telegram/ext/messagequeue.py) (it's short, self-explaining and well-commented). In fact, it's easier to understand its implementation details in Python, than in English ;). Now let's move on to the usage example.

## MessageQueue from user perspective
### Current status
For now, it's still under development, but **could be already used**. More detailed, now it's detached from other Python-Telegram-Bot lib components and therefore you should do a little extra work to use it. We plan to tightly couple it with [`telegram.Bot`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.bot.html) so that it could be used more conveniently (and even implicitly unless other specified). But anyway, **the future releases would be backwards compatible with current [`MessageQueue`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.messagequeue.html) class and `queuedmessage` decorator**.

So, feel free to use it and stay tuned for new features. We will NOT join the dark side and break the API.

### Using MQ with @queuedmessage decorator
[`MessageQueue`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.messagequeue.html) module includes a convenient `@queuedmessage` decorator, which allows to delegate the required send method calls to MQ. However, it requires you to do a little work by hand, mainly create a [`telegram.Bot`](http://python-telegram-bot.readthedocs.io/en/latest/telegram.bot.html) subclass and decorate those methods. 

Below is listed the example of its usage, which is based on echo bot from our [Tutorial](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot#your-first-bot-step-by-step). Trace through it (it's self-explanatory enough) and try experimenting with it on your own. Don't forget to look at the [`MessageQueue` docs](http://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.messagequeue.html) at the same time to clarify the dark corners. It's important that you properly understand how MQ works before using it.

```python
#!/usr/bin/env python3
# encoding=utf-8

'''
MessageQueue usage example with @queuedmessage decorator.
Provide your bot token with `TOKEN` environment variable or list it in
file `token.txt`
'''

import telegram.bot
from telegram.ext import messagequeue as mq


class MQBot(telegram.bot.Bot):
    '''A subclass of Bot which delegates send method handling to MQ'''
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super().__init__(*args, **kwargs)
        # below 2 attributes should be provided for decorator usage
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        '''Wrapped method would accept new `queued` and `isgroup`
        OPTIONAL arguments'''
        super().send_message(*args, **kwargs)


if __name__ == '__main__':
    from telegram.ext import MessageHandler, Filters
    import os
    token = os.environ.get('TOKEN') or open('token.txt').read().strip()
    # for test purposes limit global throughput to 3 messages per 3 seconds
    q = mq.MessageQueue(all_burst_limit=3, all_time_limit_ms=3000)
    testbot = MQBot(token, mqueue=q)
    upd = telegram.ext.updater.Updater(bot=testbot)

    def reply(bot, update):
        # tries to echo 10 msgs at once
        chatid = update.message.chat_id
        msgt = update.message.text
        print(msgt, chatid)
        for ix in range(10):
            bot.send_message(chat_id=chatid, text='%s) %s' % (ix + 1, msgt))

    hdl = MessageHandler(Filters.text, reply)
    upd.dispatcher.add_handler(hdl)
    upd.start_polling()

```

Which produces the following results (notice the delays happening, but be aware the timings on the figure don't precisely reflect the actual API delays):

![test_result](https://user-images.githubusercontent.com/16870636/28393529-e753ea26-6cef-11e7-981f-35b98fcddd61.png) |
---|

> **Note:** such way of MQ usage may become overkill in future as more convenient interface would be implemented, but as being said it would remain backwards-compatible.

> **Recommendations:**<br>
As stated in [`@queuedmessage` docs](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.messagequeue.html#telegram.ext.messagequeue.queuedmessage), for now the user needs to provide the `isgroup` boolean argument to wrapped methods or relay on `False` default. If you need to use MQ with group-type messages, you could determine the message type by checking `chat_id` (for group-type messages it would be < 0 ). However, this is not officially documented in [Telegram's Bot docs](https://core.telegram.org/bots/) and therefore prone to change in future. Use it on your own risk. The more reliable way is to make a request to API to determine chat type before sending message and cache the result. We're working on implementing this approach, so stay tuned.<br><br>If you're developing a multi-process bot with message sends and bot logic separated, it may come in handy to provide the `multiprocessing.Queue` instead of `queue.Queue` as argument to [`DelayQueue`](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.messagequeue.html#telegram.ext.messagequeue.DelayQueue). Be sure to start MQ manually in this case (provide `autostart=False` argument and call `start` method as needed).

### If you have any related questions
Feel free to ask on our [Telegram Channel](https://telegram.me/pythontelegrambotchannel).

Or you may directly ask the MQ responsive dev:<br>[thodnev @ Telegram](https://telegram.me/thodnev) (support in English or Russian; please, only MQ-related questions)



## What to read next?
_Check out our_ [Extensions -- JobQueue](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue). _It's amazing!_

_Probably, you would be also interested in_ [Performance Optimizations](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Performance-Optimizations) _for your bot._

_You've coded something worth sharing or just want to participate in dev process? Great! We would really appreciate that. Check out our_ [Contribution Guide](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/.github/CONTRIBUTING.rst) _for more details._