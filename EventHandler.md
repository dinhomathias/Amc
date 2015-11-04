##EventHandler

### Problem
python-telegram-bot is very good library. user has to take care of keeping the application alive, poll every interval, take care of last updated id.

### Solution
If the Bot object it self is act as event handler where it provides facility to register callbacks for commands and messages

### Threaded approach
In `BotEventListener.__init__`, we create a [synchronized Queue](https://docs.python.org/2/library/queue.html) (`updateQueue`) and pass that queue to the `Broadcaster`. `BotEventHandler` deliver the updates into the queue in the `__start`-Method. The Broadcaster continuously queries the queue for new updates in the `process`-Method and calls the Handlers in it's own thread. Both Threads are started in `BotEventHandler.start`, which also returns the `updateQueue`, which is used by the main thread to insert CLI commands. 

#### BotEventHandler class

```python
import sys
from threading import Thread
from telegram import (Bot, TelegramError, TelegramObject, NullHandler)
from broadcaster import Broadcaster
import time

# Adjust for differences in Python versions
if sys.version_info.major is 2:
    from Queue import Queue
elif sys.version_info.major is 3:
    from queue import Queue

class BotEventHandler:
    def __init__(self, token):
        self.bot = Bot(token)
        self.updateQueue = Queue()  # Create update queue to pass to Broadcaster
        self.lastUpdateId = 0
        self.broadcaster = Broadcaster(self.bot, self.updateQueue)  # Pass queue

    def start(self, pollintv=1.0):
        """ Starts the Threads """
        self.broadcasterThread = Thread(target=self.broadcaster.process, name="broadcaster")
        self.eventHandlerThread = Thread(target=self.__start, name="eventhandler", args=(pollintv,))
        
        self.broadcasterThread.daemon = True
        self.eventHandlerThread.daemon = True
        
        self.broadcasterThread.start()
        self.eventHandlerThread.start()
        return self.updateQueue  # Return the update queue so the main thread can insert updates

    def __start(self, pollintv):
        """ Thread target of thread eventhandler """
        while(True):
            updates = self.bot.getUpdates(self.lastUpdateId);
            for update in updates:
                self.updateQueue.put(update)  # Put update into queue instead of calling the process method directly
                self.lastUpdateId = update.update_id + 1
                time.sleep(pollintv)

    def stop(self):
        pass

    # Listener Registration
    def onMessage(self, listener):
        self.broadcaster.onMessage(listener)

    def onCommand(self, command, listener):
        self.broadcaster.onCommand(command, listener)
        
    def onCLICommand(self, command, listener):
        self.broadcaster.onCLICommand(command, listener)

    def onUnknownCommand(self, listener):
        self.broadcaster.onUnknownCommand(listener)

    def onError(self, listener):
        self.broadcaster.onError(listener)

````
#### Broadcaster class
```python
from telegram import (Bot, TelegramError, TelegramObject, NullHandler)

class Broadcaster:
    def __init__(self, bot, updateQueue):
        self.bot = bot
        self.updateQueue = updateQueue  # Get update queue from BotEventHandler
        self.messageListeners = []
        self.commandListeners = {}
        self.CLICommandListeners = {}
        self.unknownCommandListeners = []
        self.errorListeners = []

    # Listener Registration
    def onMessage(self, listener):
        self.messageListeners.append(listener)

    def onCommand(self, command, listener):
        self.commandListeners[command] = listener
        
    def onCLICommand(self, command, listener):
        self.CLICommandListeners[command] = listener

    def onUnknownCommand(self, listener):
        self.unknownCommandListeners.append(listener)

    def onError(self, listener):
        self.errorListeners.append(listener)

    # Broadcasting for all listeners 
    def process(self):
        """ Thread target of thread broadcaster """
        while True:
            update = self.updateQueue.get()  # Pop update from update queue. Blocks if no updates are available.
            
            if type(update) is str:  # This is a CLI update
                command = update.split(" ")[0][1:]
                self.broadcastCLICommand(command, ' '.join(update.split(" ")[1:]))
            elif update.message.text.startswith("/"):  # This is a regular update
                command = update.message.text.split(" ")[0][1:]
                self.broadcastCommand(command, update)
            else:
                self.broadcastMessage(update)

    def broadcastCommand(self, command, update):
        if command in self.commandListeners:
            listener = self.commandListeners[command]
            listener.onUpdate(self.bot, update)
        else:
           for listener in self.unknownCommandListeners:
               listener.onUpdate(self.bot, update)
    
    def broadcastCLICommand(self, command, update):
        if command in self.CLICommandListeners:
            listener = self.CLICommandListeners[command]
            listener.onUpdate(self.bot, update)
        else:
           print("Unknown command")

    def broadcastMessage(self, update):
        for listener in self.messageListeners:
            listener.onUpdate(self.bot, update)

```

### How to use

```python
import sys
from boteventhandler import BotEventHandler
from telegram import Update, Message

global last_chat_id
last_chat_id = 0

class StartCommandHandler:
    def onUpdate(self, bot, update):
        # handle the start command
        pass

class HelpCommandHandler:
    def onUpdate(self, bot, update):
        # handle the help command
        pass

class UnknownCommandHandler:
    def onUpdate(self, bot, update):
        # handle the unknown command
        pass

class MessageHandler:
    def onUpdate(self, bot, update):
        global last_chat_id
        last_chat_id = update.message.chat_id
        bot.sendMessage(update.message.chat_id, text=update.message.text)

class ErrorHandler:
    def onError(self, bot, error):
        # handle the error here
        pass

class CLIReplyCommandHandler:
    """ Demo command """
    def onUpdate(self, bot, args):
        if last_chat_id is not 0:
            bot.sendMessage(chat_id=last_chat_id, text=args)

def main():
    eh = BotEventHandler("TOKEN")

    # on different commands
    eh.onCommand("start", StartCommandHandler())
    eh.onCommand("help", HelpCommandHandler())
    
    # on CLI commands
    eh.onCLICommand("reply", CLIReplyCommandHandler())  # Register cli handler

    # on unknown command
    eh.onUnknownCommand(UnknownCommandHandler())

    # on noncommand i.e message
    eh.onMessage(MessageHandler())

    # on error
    eh.onError(ErrorHandler())

    # Start the threads and store the update Queue, so we can insert updates ourselves
    updateQueue = eh.start()
    
    # Start CLI-Loop
    while True:
        if sys.version_info.major is 2:
            text = raw_input("Input: ")
        elif sys.version_info.major is 3:
            text = input("Input: ")
            
        updateQueue.put(text)  # Put command into queue

if __name__ == '__main__':
    main()

```




    