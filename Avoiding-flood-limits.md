## What the spam limits are and why you should avoid hitting them
Considering [Telegram's Bot documentation](https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this), currently the maximum amount of messages being sent by bots is limited to 30&#160;messages/second for all ordinary messages and 20&#160;messages/minute for group messages. According to [@BotSupport](https://t.me/BotSupport) the limit for group also applies to channels (this is not confirmed by Telegram in their documentation however). When your bot hits spam limits, it starts to get 429 errors from Telegram API. And assuming that error handling in such case usually is coded as simple retrials, the running machine would spend a lot of CPU time retrying (or got locked down, depending on bot implementation details). And constantly retrying to send messages while ignoring API errors could result in your bot being banned for some time.

That means, if you're making a production-ready bot, which should serve numerous users **it's always a good idea to use throughput limiting mechanism for messages being sent**. This way you could be sure that all messages would be delivered to end-users as soon as possible in ordered way.

## Available tools and their implementation details

Currently, PTB has no built-in mechanism to avoid flood limits. The previously used `MessageQueue` was removed in v20 as it had a number of bugs and was not well integrated with the library.

Adding a new mechanism is on the roadmap.