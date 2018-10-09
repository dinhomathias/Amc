**Note: This guide is of no use to the regular user.**

### Variables:
```
CI = AppVeyor|Travis
py_platform = CPython|PyPy
py_version = 27|34|35|36|37
bot_username = ptb_{CI.lower()}_{py_platform.lower()}_{py_version.lower()}_testbot
```

## Setup a new bot

`#` means *send a message to @BotFather*  
`%` means *click button in inlinekeyboard*  

### Create the bot

`# /newbot`  
`# Python-telegram-bot tests on {CI} {py_platform} {py_version}` *(Bot name)*  
`# {bot_username}` *(Bot username)*  

The token for the new bot will be shown.

### Set texts in case a user stumbles upon the bot

`# /set_description`  
`# @{bot_username}`  
`# This bot is only for running tests for python-telegram-bot and has no actual functionality.`  

`# /set_abouttext`  
`# @{bot_username}`  
`# This bot is only for running tests for python-telegram-bot and has no actual functionality.`  

### Turn on inline so we can create a game for the bot

`# /set_inline`  
`# @{bot_username}`  
`# This bot is only for running tests. {CI} {py_platform} {py_version}`  

### Create a game for the bot

`# /newgame`  
`# OK`  
`# Accept`  
`# @{bot_username}`  
`# Python-telegram-bot test game`  
`# A no-op test game, for python-telegram-bot bot framework testing.`  
`Upload tests/data/game.png`  
`Upload tests/data/game.gif`  
`# test_game`  

### Payment
Now we need to setup payment. This can only be done via the beta /mybots interface.

`#mybots`  
`% @{bot_username}`  
`% Payments`  
`% Stripe` *(might have a flag in front, depending on your country)*  
`% Connect Stripe Test`  
`Press start in @StripeTestBot`  
`% Authorize`  
`Press "Skip this account form" at the top of your browser`  
`Go back to @StripeTestBot and make sure everything went well`  
`Go back to @BotFather`  

The payment provider token should be displayed in the last message.


