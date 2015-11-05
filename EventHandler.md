##EventHandler

### Problem
python-telegram-bot is very good library. user has to take care of keeping the application alive, poll every interval, take care of last updated id.

### Solution
If the Bot object it self is act as event handler where it provides facility to register callbacks for commands and messages

### Threaded approach
In `BotEventListener.__init__`, we create a [synchronized Queue](https://docs.python.org/2/library/queue.html) (`update_queue`) and pass that queue to the `Broadcaster`. `BotEventHandler` deliver the updates into the queue in the `__start`-Method. The Broadcaster continuously queries the queue for new updates in its own `start`-Method and calls the Handlers in it's own thread. Both Threads are started in `BotEventHandler.start`, which also returns the `update_queue`, that then can be used by the main thread to insert CLI commands (in this example). 

#### BotEventHandler class

```python
#!/usr/bin/env python

"""
This module contains the class BotEventHandler, which tries to make creating 
Telegram Bots intuitive!
"""

import sys
from threading import Thread
from telegram import (Bot, TelegramError, TelegramObject)
from broadcaster import Broadcaster
import time

# Adjust for differences in Python versions
if sys.version_info.major is 2:
    from Queue import Queue
elif sys.version_info.major is 3:
    from queue import Queue

class BotEventHandler(TelegramObject):
    """
    This class provides a backend to telegram.Bot to the programmer, so they can
    focus on coding the bot. I also runs in a seperate thread, so the user can
    interact with the bot, for example on the command line. It supports Handlers
    for different kinds of data: Updates from Telegram, basic text commands and
    even arbitrary types.
    
    Attributes:
    
    Args:
        token (str): The bots token given by the @BotFather
        **kwargs: Arbitrary keyword arguments.

    Keyword Args:
        base_url (Optional[str]):
    """
    
    def __init__(self, token, base_url=None):
        self.bot = Bot(token, base_url)
        self.update_queue = Queue()
        self.last_update_id = 0
        self.broadcaster = Broadcaster(self.bot, self.update_queue)

    # Add Handlers
    def addMessageHandler(self, handler):
        """
        Registers a message handler in the Broadcaster.
        
        Args:
            handler (function): A function that takes (Bot, Update) as
                arguments.
        """
        
        self.broadcaster.addMessageHandler(handler)

    def addCommandHandler(self, command, handler):
        """
        Registers a command handler in the Broadcaster.
        
        Args:
            command (str): The command keyword that this handler should be 
                listening to. 
            handler (function): A function that takes (Bot, Update) as
                arguments.
        """
        
        self.broadcaster.addCommandHandler(command, handler)

    def addTextCommandHandler(self, command, handler):
        """
        Registers a text-command handler in the Broadcaster.

        Args:
            command (str): The command keyword that this handler should be
                listening to.
            handler (function): A function that takes (Bot, str) as arguments.
        """
        
        self.broadcaster.addTextCommandHandler(command, handler)

    def addUnknownCommandHandler(self, handler):
        """
        Registers a command handler in the Broadcaster, that will receive all
        commands that have no associated handler.

        Args:
            handler (function): A function that takes (Bot, Update) as
                arguments.
        """
        
        self.broadcaster.addUnknownCommandHandler(handler)

    def addUnknownTextCommandHandler(self, handler):
        """
        Registers a text-command handler in the Broadcaster, that will receive 
        all commands that have no associated handler.
        
        Args:
            handler (function): A function that takes (Bot, str) as arguments.
        """
        
        self.broadcaster.addUnknownTextCommandHandler(handler)
        
    def addErrorHandler(self, handler):
        """
        Registers an error handler in the Broadcaster.
        
        Args:
            handler (function): A function that takes (Bot, TelegramError) as
                arguments.
        """
        
        self.broadcaster.addErrorHandler(handler)

    def addTypeHandler(self, the_type, handler):
        """
        Registers a type handler in the Broadcaster. This allows you to send
        any type of object into the update queue.

        Args:
            the_type (type): The type this handler should listen to
            handler (function): A function that takes (Bot, type) as arguments.
        """

        self.broadcaster.addTypeHandler(the_type, handler)

    # Remove Handlers
    def removeMessageHandler(self, handler):
        """
        De-Registers a message handler in the Broadcaster.

        Args:
            handler (obj):
        """

        self.broadcaster.removeMessageHandler(handler)

    def removeCommandHandler(self, command, handler):
        """
        De-Registers a command handler in the Broadcaster.

        Args:
            command (str): The command that the handler is listening to.

            handler (any): An object that implements the onUpdate(Bot, Update)
                method.
        """

        self.broadcaster.removeCommandHandler(command, handler)

    def removeTextCommandHandler(self, command, handler):
        """
        De-Registers a command handler in the Broadcaster.

        Args:
            command (str): The text-command that the handler is listening to.
            handler (any):
        """

        self.broadcaster.removeTextCommandHandler(command, handler)

    def removeUnknownCommandHandler(self, handler):
        """
        De-Registers a command handler in the Broadcaster.

        Args:
            handler (any):
        """

        self.broadcaster.removeUnknownCommandHandler(handler)

    def removeUnknownTextCommandHandler(self, handler):
        """
        De-Registers a text-command handler in the Broadcaster.

        Args:
            handler (any):
        """

        self.broadcaster.removeUnknownTextCommandHandler(handler)

    def removeErrorHandler(self, handler):
        """
        De-Registers an error handler in the Broadcaster.

        Args:
            handler (any):
        """

        self.broadcaster.removeErrorHandler(handler)

    def removeTypeHandler(self, the_type, handler):
        """
        De-registers a type handler.

        Args:
            handler (any):
        """

        self.broadcaster.removeTypeHandler(the_type, handler)

    def start(self, poll_interval=1.0):
        """
        Starts polling updates from Telegram. 
        
        Args:
            **kwargs: Arbitrary keyword arguments.

        Keyword Args:
            poll_interval (Optional[float]): Time to wait between polling 
                updates from Telegram in seconds. Default is 1.0
        """

        # Create Thread objects
        broadcaster_thread = Thread(target=self.broadcaster.start,
                                    name="broadcaster")
        event_handler_thread = Thread(target=self.__start, name="eventhandler",
                                      args=(poll_interval,))

        # Set threads as daemons so they'll stop if the main thread stops
        broadcaster_thread.daemon = True
        event_handler_thread.daemon = True
        
        # Start threads
        broadcaster_thread.start()
        event_handler_thread.start()
        
        # Return the update queue so the main thread can insert updates
        return self.update_queue

    def __start(self, poll_interval):
        """
        Thread target of thread 'eventhandler'. Runs in background, pulls
        updates from Telegram and inserts them in the update queue of the
        Broadcaster.
        """

        while True:
            try:
                updates = self.bot.getUpdates(self.last_update_id)
                for update in updates:
                    self.update_queue.put(update)
                    self.last_update_id = update.update_id + 1
                    time.sleep(poll_interval)
            except TelegramError as te:
                # Put the error into the update queue and let the Broadcaster
                # broadcast it
                self.update_queue.put(te)
                time.sleep(poll_interval)
````
#### Broadcaster class
```python
#!/usr/bin/env python
from telegram import (TelegramError, TelegramObject, Update)

class Broadcaster(TelegramObject):
    def __init__(self, bot, update_queue):
        self.bot = bot
        self.update_queue = update_queue
        self.message_handlers = []
        self.command_handlers = {}
        self.text_command_handlers = {}
        self.type_handlers = {}
        self.unknown_command_handlers = []
        self.unknown_text_command_handlers = []
        self.error_handlers = []

    # Add Handlers
    def addMessageHandler(self, handler):
        """
        Registers a message handler in the Broadcaster.
        
        Args:
            handler (function): A function that takes (Bot, Update) as
                arguments.
        """
        
        self.message_handlers.append(handler)

    def addCommandHandler(self, command, handler):
        """
        Registers a command handler in the Broadcaster.
        
        Args:
            command (str): The command keyword that this handler should be 
                listening to. 
            handler (function): A function that takes (Bot, Update) as
                arguments.
        """
        
        if command not in self.command_handlers:
            self.command_handlers[command] = []
            
        self.command_handlers[command].append(handler)
        
    def addTextCommandHandler(self, command, handler):
        """
        Registers a text-command handler in the Broadcaster.
        
        Args:
            command (str): The command keyword that this handler should be 
                listening to. 
            handler (function): A function that takes (Bot, str) as arguments.
        """
        
        if command not in self.text_command_handlers:
            self.text_command_handlers[command] = []

        self.text_command_handlers[command].append(handler)

    def addUnknownCommandHandler(self, handler):
        """
        Registers a command handler in the Broadcaster, that will receive all
        commands that have no associated handler.
        
        Args:
            handler (function): A function that takes (Bot, Update) as
                arguments.
        """
        
        self.unknown_command_handlers.append(handler)
        
    def addUnknownTextCommandHandler(self, handler):
        """
        Registers a text-command handler in the Broadcaster, that will receive 
        all commands that have no associated handler.
        
        Args:
            handler (function): A function that takes (Bot, str) as arguments.
        """
        
        self.unknown_text_command_handlers.append(handler)

    def addErrorHandler(self, handler):
        """
        Registers an error handler in the Broadcaster.
        
        Args:
            handler (function): A function that takes (Bot, TelegramError) as
                arguments.
        """
        
        self.error_handlers.append(handler)

    def addTypeHandler(self, the_type, handler):
        """
        Registers a type handler in the Broadcaster. This allows you to send
        any type of object into the update queue.
        
        Args:
            the_type (type): The type this handler should listen to
            handler (function): A function that takes (Bot, type) as arguments.
        """

        if the_type not in self.type_handlers:
            self.type_handlers[the_type] = []
        
        self.type_handlers[the_type].append(handler)

    # Remove Handlers
    def removeMessageHandler(self, handler):
        """
        De-registers a message handler.
        
        Args:
            handler (any):
        """

        if handler in self.message_handlers:
            self.message_handlers.remove(handler)
        
    def removeCommandHandler(self, command, handler):
        """
        De-registers a command handler.
        
        Args:
            command (str): The command
            handler (any):
        """

        if command in self.command_handlers \
                and handler in self.command_handlers[command]:
            self.command_handlers[command].remove(handler)

    def removeTextCommandHandler(self, command, handler):
        """
        De-registers a text-command handler.

        Args:
            command (str): The command
            handler (any):
        """

        if command in self.text_command_handlers \
                and handler in self.text_command_handlers[command]:
            self.text_command_handlers[command].remove(handler)

    def removeUnknownCommandHandler(self, handler):
        """
        De-registers an unknown-command handler.

        Args:
            handler (any):
        """

        if handler in self.unknown_command_handlers:
            self.unknown_command_handlers.remove(handler)

    def removeUnknownTextCommandHandler(self, handler):
        """
        De-registers an unknown-command handler.

        Args:
            handler (any):
        """

        if handler in self.unknown_text_command_handlers:
            self.unknown_text_command_handlers.remove(handler)

    def removeErrorHandler(self, handler):
        """
        De-registers an error handler.

        Args:
            handler (any):
        """

        if handler in self.error_handlers:
            self.error_handlers.remove(handler)

    def removeTypeHandler(self, the_type, handler):
        """
        De-registers a type handler. 
        
        Args:
            handler (any):
        """

        if the_type in self.type_handlers \
                and handler in self.type_handlers[the_type]:
            self.type_handlers[the_type].remove(handler)
        
    def start(self):
        """
        Thread target of thread 'broadcaster'. Runs in background and processes
        the update queue.
        """
        
        while True:
            try:
                # Pop update from update queue.
                # Blocks if no updates are available.
                update = self.update_queue.get()
                self.processUpdate(update)
            
            # Broadcast any errors
            except TelegramError as te:
                self.broadcastError(te)

    def processUpdate(self, update):
        """
        Processes a single update.

        Args:
            update (any):
        """

        # Custom type handlers can override Text handlers
        if type(update) in self.type_handlers:
            self.broadcastType(update)

        # text update
        elif type(update) is str:
            self.broadcastTextCommand(update)

        # An error happened while polling
        elif type(update) is TelegramError:
            self.broadcastError(update)

        # Telegram update (command)
        elif type(update) is Update \
                and update.message.text.startswith('/'):
            self.broadcastCommand(update)

        # Telegram update (message)
        elif type(update) is Update:
            self.broadcastMessage(update)

        # Update not recognized
        else:
            self.broadcastError(TelegramError(
                "Received update of unknown type %s" % type(update)))

    def broadcastCommand(self, update):
        """
        Broadcasts an update that contains a command. 
        
        Args:
            command (str): The command keyword
            update (TelegramUpdate): The Telegram update that contains the
                command
        """
        
        command = update.message.text.split(' ')[0][1:].split('@')[0]
        
        if command in self.command_handlers:
            self.broadcastTo(self.command_handlers[command], update)
        else:
            self.broadcastTo(self.unknown_command_handlers, update)
    
    def broadcastTextCommand(self, update):
        """
        Broadcasts a text-update that contains a command. 
        
        Args:
            update (str): The text input
        """
        
        command = update.split(' ')[0]
        
        if command in self.text_command_handlers:
            self.broadcastTo(self.text_command_handlers[command], update)
        else:
            self.broadcastTo(self.unknown_text_command_handlers, update)
    
    def broadcastType(self, update):
        """
        Broadcasts a text-update that contains a command. 
        
        Args:
            update (str): The text input
        """
        
        t = type(update)
        
        if t in self.type_handlers:
            self.broadcastTo(self.type_handlers[t], update)
        else:
            self.broadcastError(TelegramError(
                "Received update of unknown type %s" % type(update)))
    
    def broadcastMessage(self, update):
        """
        Broadcasts an update that contains a regular message. 
        
        Args:
            update (TelegramUpdate): The Telegram update that contains the
                message.
        """
        
        self.broadcastTo(self.message_handlers, update)

    def broadcastError(self, error):
        """
        Broadcasts an error.

        Args:
            error (TelegramError): The Telegram error that was raised.
        """

        for handler in self.error_handlers:
            handler(self.bot, error)

    def broadcastTo(self, handlers, update):
        """
        Broadcasts an update to a list of handlers.

        Args:
            handlers (list): A list of handler-functions.
            update (any): The update to be broadcasted
        """

        for handler in handlers:
            handler(self.bot, update)
```

### How to use

```python
#!/usr/bin/env python

import sys
from boteventhandler import BotEventHandler

global last_chat_id
last_chat_id = 0

def removeCommand(text):
    return ' '.join(text.split(' ')[1:])

def startCommandHandler(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')

def helpCommandHandler(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')

def unknownCommandHandler(bot, update):
    bot.sendMessage(update.message.chat_id, text='Sorry, I do not understand!')

def messageHandler(bot, update):
    global last_chat_id
    last_chat_id = update.message.chat_id
    print(update.message.text)
    bot.sendMessage(update.message.chat_id, text=update.message.text)

def errorHandler(bot, error):
    print(str(error))

# Demo command. Replies to last active chat_id.
def CLIReplyCommandHandler(bot, update):
    if last_chat_id is not 0:
        bot.sendMessage(chat_id=last_chat_id, text=removeCommand(update))

# Demo command
def unknownCLICommandHandler(bot, update):
    print("I did not understand %s" % update)

def main():
    eh = BotEventHandler("TOKEN")

    # on different commands
    eh.addCommandHandler("start", startCommandHandler)
    eh.addCommandHandler("help", helpCommandHandler)
    
    # on CLI commands
    eh.addTextCommandHandler("reply", CLIReplyCommandHandler)

    # on unknown commands
    eh.addUnknownCommandHandler(unknownCommandHandler)

    # on unknown CLI commands
    eh.addUnknownTextCommandHandler(unknownCLICommandHandler)

    # on noncommand i.e message
    eh.addMessageHandler(messageHandler)

    # on error
    eh.addErrorHandler(errorHandler)

    # Start the threads and store the update Queue,
    # so we can insert updates ourselves
    update_queue = eh.start()
    
    # Start CLI-Loop
    while True:
        if sys.version_info.major is 2:
            text = raw_input()
        elif sys.version_info.major is 3:
            text = input()
        
        if len(text) > 0:
            update_queue.put(text)  # Put command into queue

if __name__ == '__main__':
    main()
```




    