##EventHandler

### Problem
python-telegram-bot is very good library. user has to take care of keeping the application alive, poll every interval, take care of last updated id.

### Solution
If the Bot object it self is act as event handler where it provides facility to register callbacks for commands and messages

### proposed Changes
`
class BotEventHandler:
    pass
`