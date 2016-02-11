##Conversation

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

class Conversations(object):
    