python-telegram-bot provides bot interaction with telegram. While having this beautiful library, It will be good if we have a conversation also integrated in to library.

or written a external library people can use it along with python-telegram-bot.

### Problem
if a user is conversing with bot, he will have to write a entire state machine to facilitate this conversation.
take an example, if a bot want to request few details, email id, first name, last name, telephone, address from user, 
then there will be a lot of if and else statement.

### Solution that i can think of

Conversation is unique per chat_id, and if we assume each to and fro communication is Chat

```python
#!/usr/bin/env python

#Base chat
class TelegramChat(object):

    def name(self):
        return self.__class__.__name__

    def can(self, userresponse):
        return True

    def from_user(self, update, cwf):
        pass

    def to_user(self, cwf):
        pass

    def markup(self):
        return telegram.ReplyKeyboardHide()

# Chat store
class Chats(object):

    def __init__(self):
        self.chats = {}

    def add(self, tgchat):
        self.chats[tgchat.name()] = tgchat

    def get(self, tgchatname):
        if  tgchatname in self.chats:
            return self.chats[tgchat.name()]
        else:
            return None

class TelegramConversation(object):

    def __init__(self, chats, chat_id, user=None):
        self.chats = chats
        self.chat_id = chat_id
        self.user = user
        self.currentchat = self.chats.get("Start")

    def processUpdate(self, update):
        self.currentchat.from_user(update)

# Conversation store
class TelegramConversations(object):

    def __init__(self, chats):
        self.conversations = []
        self.chats = chats

    def get(self, chat_id, user=None):
        if chat_id not in self.conversations:
            self.conversations[chat_id] = TelegramConversation(self.chats, chat_id, user)

        return self.conversations[chat_id]

    def processUpdate(self, update):
        conversation = self.get(update.message.chat_id)
        conversation.processUpdate(update)