# How to ask good technical questions

When working with PTB, you will sooner or later have a question. And that's fine! You can only expand your knowledge by asking questions and getting answers.
This article is about *how to ask good questions*, focusing on questions appearing when working with PTB.
Before we begin, please try to keep one rule of thumb in mind:

> You want something from somebody else, so please put some effort in it.

Putting effort in it makes it easier for others to actually help you and it's more pleasant for both sides ;)

Errors/questions can appear on a lot of different levels and need to be addressed differently. 

## General Python questions & Questions about other libraries

When you're coding a bot, you will have to code a lot of stuff that doesn't actually have to do anything with PTB, i.e. the backend. 
Maybe you're also using other python libraries.

Please be aware that neither the PTBs user group on Telegram nor the issue tracker on PTBs GitHub repository are the right place to ask those questions.

## Design Questions

Many questions are not about how to use a specific method/class of PTB, but more along the lines "If a users does this, I want my bot to react like that. What can I use for that?".
When asking how to build a specific functionality with PTB, please try to describe it precisely and include all relevant information. Answering the following questions usually is a good starting point:

1. What kind of event should trigger the functionality? Possible triggers are e.g.
    * User sends a message containing a command/specific expression/an image/…
    * A new member joins the group
    * A user presses an `InlineKeyboardButton`
    * A specific time of the day
    * Bot starts running
2. What kind of chat is the functionality supposed to work in? A private chat with the bot? A group/supergroup? Or a channel?
3. Is your Bot an Admin in that Chat?
4. How do you want your bot to react?

### A Bad Example:

> How do I verify a user?

### A Good Example:

> When a new user enters a group, where my bot is an admin, I would like to verify that they are not spam bots by having them fill out some kind of captcha, preferably in the private chat with the bot. If the captcha is not filled out correctly within one day, they should be banned. How can I set up something like this?

## Questions on PTB

You have set up your bot - but something doesn't work. An update is not processed as you would expect it to be or you're encountering an error.
Again, please try to be precise and include all relevant information. This means:

1. What would you expect to happen? Usually this includes
  * What kind of update are you processing? Message, InlineQuery, CallbackQuery, …?
  * What kind of handler did you set up to handle this? What is it supposed to do?
2. What is actually happening?
  * If you're encountering an exception, please provide the full [traceback](https://realpython.com/python-traceback/)
  * Make sure that you activate [logging](https://github.com/python-telegram-bot/python-telegram-bot/#logging) or an [[error handler|Exception-Handling]] so that you can actually see the traceback!
3. Where exactly are things going south? If you can locate the line/s of code that are misbehaving, please include them in your question.
  
If you have a hard time laying your finger on where exactly things go south, it might be helpful to provide a [minimal working example](https://telegra.ph/Minimal-Working-Example-for-PTB-07-18).

### A Bad Example:

> The bot does not work and the messages do not connect to me.

### A Good Example:

> When using my bot in private it responds to all messages as expected. When I add it to a group, it doesn't, although I don't see any error messages in the log. How can I fix this?
