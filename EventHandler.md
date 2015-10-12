##EventHandler

### Problem
python-telegram-bot is very good library. user has to take care of keeping the application alive, poll every interval, take care of last updated id.

### Solution
If the Bot object it self is act as event handler where it provides facility to register callbacks for commands and messages

#### BotEventHandler class

```python
class BotEventHandler:
    def __init__(token, base_url=None):
        self.bot = Bot(token, base_url)
        self.lastUpdateId = 0
        self.broadcaster = Broadcaster(self.bot)

    def start(self, pollintv=1.0):
        while(True):
            updates = self.bot.getUpdates(self.lastUpdateId);
            for update in updates;
                self.broadcaster.process(update)
                self.lastUpdateId = update.update_id
                sleep(pollintv)

    def stop(self):
        pass

    # Listener Registration
    def onMessage(self, listener):
        self.broadcaster.onMessage(listener)

    def onCommand(self, command, listener):
        self.broadcaster.onCommand(listener)

    def onUnknownCommand(self, listener):
        self.broadcaster.onUnknownCommand(listener)

    def onError(self, listener):
        self.broadcaster.onError(listener)

````
#### Broadcaster class
```python
class Broadcaster:
    def __init__(self, bot):
        self.bot = bot
        self.messageListeners = []
        self.commandListeners = {}
        self.unknownCommandListeners = []
        self.errorListeners = []

    # Listener Registration
    def self.onMessage(self, listener):
        self.messageListener.append(listener)

    def self.onCommand(self, command, listener):
        self.commandListener[command] = listener

    def self.onUnknownCommand(self, listener):
        self.unknownCommandListener .append(listener)

    def self.onError(self, listener):
        self.unknownCommandListener .append(listener)

    # Broadcasting for all listeners 
    def process(self, update):
        msg = update.message.text
        if msg.startswith("/"):
            command = msg.split("/")[0]
            broadcastCommand(command, update)
        else:
            broadcastMessage(update)

    def broadcastCommand(self, command, update):
        if command in self.commandListeners:
            listener = self.commandListeners[command]
            listener.onUpdate(self.bot, update)
        else:
           for listener in self.unknownCommandListeners:
               listener.onUpdate(self.bot, update)

    def broadcastMessage(self, update):
        for listener in self.unknownCommandListeners:
            listener.onUpdate(self.bot, update)
```

### How to use

```python
class StartCommandHandler:
    def onUpdate(bot, update):
       # handle the start command
       pass

class HelpCommandHandler:
    def onUpdate(bot, update):
       # handle the help command
       pass

class UnknownCommandHandler:
    def onUpdate(bot, update):
       # handle the unknown command
       pass

class MessageHandler:
    def onUpdate(bot, update):
       # handle the messages
       pass

class ErrorHander:
    def onError(bot, error):
       # handle the error here
       pass

def main():
    eh = BotEventHandler(<token>)

    # on different commands
    eh.onCommand("start", StartCommandHandler())
    eh.onCommand("help", HelpCommandHandler())

    # on unknown command
    eh.onUnknownCommand(UnknownCommandHandler())

    # on noncommand i.e message
    eh.onMessage(MessageHandler())

    # on noncommand i.e message
    eh.onMessage(MessageHandler())

    # on error
    eh.onError(ErrorHandler())
 
    eh.start()

if __name__ == '__main__':
    main()
```




    