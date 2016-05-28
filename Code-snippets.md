This page can be read on its own, to find the code snippet you need right now. 

It is also a follow-up to the page [Introduction to the API](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API). If you come from there, you can leave your command line open and just try out a few of these snippets.


#### Fetch updates (pure API)
To fetch messages sent to your Bot, you can use the [getUpdates](https://core.telegram.org/bots/api#getupdates) API method.

_Note: _ You don't have to use `getUpdates` if you are writing your bot with the `telegram.ext` submodule, since `telegram.ext.Updater` takes care of fetching all updates for you. Read more about that [here]().

```python
>>> updates = bot.getUpdates()
>>> print([u.message.text for u in updates])
```

To fetch images sent to your Bot:

```python
>>> updates = bot.getUpdates()
>>> print([u.message.photo for u in updates if u.message.photo])
```

To reply messages you'll always need the `chat_id`:

```python
>>> chat_id = bot.getUpdates()[-1].message.chat_id
```

#### General code snippets
These snippets apply to both ways of fetching updates. If you're using `telegram.ext`, you can get the `chat_id` in your handler callback with `update.message.chat_id`.

_Note: _ In general, you can send messages to users by passing their user id as the `chat_id`. 
If the bot has a chat with the user, it will send the message to that chat.


To post a text message:

```python
>>> bot.sendMessage(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")
```

To post a text message with markdown:

```python
>>> bot.sendMessage(chat_id=chat_id, 
...                 text="*bold* _italic_ [link](http://google.com).", 
...                 parse_mode=telegram.ParseMode.MARKDOWN)
```

To post a text message with HTML formatting:

```python
>>> bot.sendMessage(chat_id=chat_id, 
...                 text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', 
...                 parse_mode=telegram.ParseMode.HTML)
```

To post an Emoji (special thanks to [Tim Whitlock](http://apps.timwhitlock.info/emoji/tables/unicode)):

```python
>>> bot.sendMessage(chat_id=chat_id, text=telegram.Emoji.PILE_OF_POO)
```

To post an image file from disk:

```python
>>> bot.sendPhoto(chat_id=chat_id, photo=open('tests/test.png', 'rb'))
```

To post a voice file from disk:

```python
>>> bot.sendVoice(chat_id=chat_id, voice=open('tests/telegram.ogg', 'rb'))
```

To post a file from an URL, this library offers a shortcut. 
You can pass the URL of the file, instead of downloading the file first. 
If you do that, the file will be downloaded and directly streamed into the response to Telegram.

```python
>>> bot.sendPhoto(chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')
```

To tell the user that something is happening on bot's side:

```python
>>> bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
```

To create [Custom Keyboards](https://core.telegram.org/bots#keyboards):

```python
>>> custom_keyboard = [[ telegram.Emoji.THUMBS_UP_SIGN,
...                      telegram.Emoji.THUMBS_DOWN_SIGN ]]
>>> reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
>>> bot.sendMessage(chat_id=chat_id, text="Stay here, I'll be back.", reply_markup=reply_markup)
```

To hide the keyboard:

```python
>>> reply_markup = telegram.ReplyKeyboardHide()
>>> bot.sendMessage(chat_id=chat_id, text="I'm back.", reply_markup=reply_markup)
```

To download a file (you will need its `file_id`):

```python
>>> file_id = message.voice.file_id
>>> newFile = bot.getFile(file_id)
>>> newFile.download('voice.ogg')
```

There are many more API methods, to read the full API documentation visit the [Telegram API documentation](https://core.telegram.org/bots/api) or the [library documentation of telegram.Bot](http://pythonhosted.org/python-telegram-bot/telegram.bot.html)

#### What to read next?
If you haven't read the tutorial "[Extensions – Your first Bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-–-Your-first-Bot)" yet, you might want to do it now.

There will be a FAQ page coming soon, as well.