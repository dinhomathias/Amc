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

    def onMessage(listener):
        self.broadcaster.onMessage(listener)

    def onCommand(command, listener):
        self.broadcaster.onMessage(listener)

    def start(self, pollintv=1.0):
        while(True):
            updates = self.bot.getUpdates(self.lastUpdateId);
            for update in updates;
                self.broadcaster.process(update)
                self.lastUpdateId = update.update_id
                sleep(2)

    def stop(self, ):
        pass
````

#### Broadcaster class
```python
class Broadcaster:
    def __init__(self, bot):
        self.bot = bot
        self.messageListener = []
        self.commandListener = {}
        self.unknownCommandListener = []

    def process(self, update):
        self.

    def self.onMessage(listener):
        self.messageListener.append(listener)

    def self.onCommandMessage(command, listener):
        self.commandListener[command] = listener

    def self.onUnknownCommandMessage(command, listener):
        self.unknownCommandListener .append(listener)
````
#### Broadcaster class