
### Can my Bot receive messages in a channel?

**No.** The Telegram Bot API has no way for a bot to receive messages in a channel. 
To prevent [two bots getting stuck in a loop replying to each other](https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots), bots can not receive any messages sent by other bots. In a channel, the source of a message is unknown - it could always be a bot.