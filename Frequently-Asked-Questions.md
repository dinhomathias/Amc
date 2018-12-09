### What messages can my Bot see?

From the official [Telegram Bot FAQ](https://core.telegram.org/bots/faq#what-messages-will-my-bot-get):
***

> **All bots, regardless of settings, will receive:**
>
> * All service messages.
> * All messages from private chats with users.
> * All messages from channels where they are a member.
>
> **Bot admins and bots with privacy mode disabled will receive all messages except messages sent by other bots.**
> 
> **Bots with privacy mode enabled will receive:**
> 
> * Commands explicitly meant for them (e.g., /command@this_bot).
> * General commands from users (e.g. /start) if the bot was the last bot to send a message to the group.
> * Messages sent via this bot.
> * Replies to any messages implicitly or explicitly meant for this bot.
> 
> **Note that each particular message can only be available to one privacy-enabled bot at a time, i.e., a reply to bot A containing an explicit command for bot B or sent via bot C will only be available to bot A. Replies have the highest priority.**
***

### What about messages from other Bots?
***
> Bots talking to each other could potentially get stuck in unwelcome loops. To avoid this, we decided that bots will not be able to see messages from other bots regardless of mode.
>
***

### Can my bot delete messages from the user in a private chat?

No.