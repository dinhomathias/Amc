This page can be read on its own to find the code snippet you need right now. 

It is also a follow-up to the page [Introduction to the API](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API). If you come from there, you can leave your command line open and just try out a few of these snippets.

- [Pure API](#pure-api)
    + [Fetch updates](#fetch-updates)
    + [Fetch images sent to your Bot](#fetch-images-sent-to-your-bot)
    + [Reply to messages](#reply-to-messages)
- [General code snippets](#general-code-snippets)
    + [Post a text message](#post-a-text-message)
    + [Reply to a message](#reply-to-a-message)
    + [Post a text message with Markdown formatting](#post-a-text-message-with-markdown-formatting)
    + [Post a text message with HTML formatting](#post-a-text-message-with-html-formatting)
    + [Post an image file from disk](#post-an-image-file-from-disk)
    + [Post a voice file from disk](#post-a-voice-file-from-disk)
    + [Post a photo from a URL](#post-a-photo-from-a-url)
    + [Post an audio from disk](#post-an-audio-from-disk)
    + [Post a file from disk](#post-a-file-from-disk)
    + [Send a chat action](#send-a-chat-action)
    + [Custom Keyboards](#custom-keyboards)
    + [Requesting location and contact from user](#requesting-location-and-contact-from-user)
    + [Hide a custom keyboard](#hide-a-custom-keyboard)
    + [Download a file](#download-a-file)
    + [Message entities](#message-entities)
- [Advanced snippets](#advanced-snippets)
    + [Restrict access to a handler (decorator)](#restrict-access-to-a-handler-decorator)
      - [Usage](#usage)
    + [Cached Telegram group administrator check](#cached-telegram-group-administrator-check)
    + [Build a menu with Buttons](#build-a-menu-with-buttons)
      - [Usage](#usage-1)
    + [Simple way of restarting the bot](#simple-way-of-restarting-the-bot)
- [What to read next?](#what-to-read-next)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>


## Pure API

#### Fetch updates
To fetch messages sent to your Bot, you can use the [getUpdates](https://core.telegram.org/bots/api#getupdates) API method.

**Note:** You don't have to use `getUpdates` if you are writing your bot with the `telegram.ext` submodule, since `telegram.ext.Updater` takes care of fetching all updates for you. Read more about that [here](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot).

```python
>>> updates = bot.getUpdates()
>>> print([u.message.text for u in updates])
```

#### Fetch images sent to your Bot

```python
>>> updates = bot.getUpdates()
>>> print([u.message.photo for u in updates if u.message.photo])
```

#### Reply to messages
You'll always need the `chat_id`

```python
>>> chat_id = bot.getUpdates()[-1].message.chat_id
```

## General code snippets
These snippets usually apply to both ways of fetching updates. If you're using `telegram.ext`, you can get the `chat_id` in your handler callback with `update.message.chat_id`.

**Note:** In general, you can send messages to users by passing their user id as the `chat_id`. 
If the bot has a chat with the user, it will send the message to that chat.


#### [Post a text message](https://core.telegram.org/bots/api#sendmessage)

```python
>>> bot.sendMessage(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")
```

#### Reply to a message

This is a shortcut to `bot.sendMessage` with sane defaults. Read more about it [in the docs](http://python-telegram-bot.readthedocs.io/en/latest/telegram.html#telegram.Message.reply_text). 

```python
>>> update.message.reply_text("I'm sorry Dave I'm afraid I can't do that.")
```

**Note:** There are equivalents of this method for replying with photos, audio etc., and similar shortcuts exist throughout the library. Related PRs: [#362](https://github.com/python-telegram-bot/python-telegram-bot/pull/362), [#420](https://github.com/python-telegram-bot/python-telegram-bot/pull/420), [#423](https://github.com/python-telegram-bot/python-telegram-bot/pull/423)

#### [Post a text message with Markdown formatting](https://core.telegram.org/bots/api#sendmessage)

```python
>>> bot.sendMessage(chat_id=chat_id, 
...                 text="*bold* _italic_ `fixed width font` [link](http://google.com).", 
...                 parse_mode=telegram.ParseMode.MARKDOWN)
```

#### [Post a text message with HTML formatting](https://core.telegram.org/bots/api#sendmessage)

```python
>>> bot.sendMessage(chat_id=chat_id, 
...                 text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', 
...                 parse_mode=telegram.ParseMode.HTML)
```

#### [Post an image file from disk](https://core.telegram.org/bots/api#sendphoto)

```python
>>> bot.sendPhoto(chat_id=chat_id, photo=open('tests/test.png', 'rb'))
```

#### [Post a voice file from disk](https://core.telegram.org/bots/api#sendvoice)

```python
>>> bot.sendVoice(chat_id=chat_id, voice=open('tests/telegram.ogg', 'rb'))
```

#### [Post a photo from a URL](https://core.telegram.org/bots/api#sendphoto)

```python
>>> bot.sendPhoto(chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')
```

#### [Post an audio from disk](https://core.telegram.org/bots/api#sendaudio)

```python
>>> bot.sendAudio(chat_id=chat_id, audio=open('tests/test.mp3', 'rb'))
```

#### [Post a file from disk](https://core.telegram.org/bots/api#senddocument)

```python
>>> bot.sendDocument(chat_id=chat_id, document=open('tests/test.zip', 'rb'))
```

#### [Send a chat action](https://core.telegram.org/bots/api#sendchataction)
Use this to tell the user that something is happening on the bot's side:

```python
>>> bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)
```

#### [Custom Keyboards](https://core.telegram.org/bots#keyboards):

```python
>>> custom_keyboard = [['top-left', 'top-right'], 
...                    ['bottom-left', 'bottom-right']]
>>> reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
>>> bot.sendMessage(chat_id=chat_id, 
...                 text="Custom Keyboard Test", 
...                 reply_markup=reply_markup)
```

See also: [Build a  menu with Buttons](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets#build-a-menu-with-buttons)

#### Requesting location and contact from user

```python
>>> location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
>>> contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
>>> custom_keyboard = [[ location_keyboard, contact_keyboard ]]
>>> reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
>>> bot.sendMessage(chat_id=chat_id, 
...                 text="Would you mind sharing your location and contact with me?", 
...                 reply_markup=reply_markup)
```

#### Hide a custom keyboard

```python
>>> reply_markup = telegram.ReplyKeyboardHide()
>>> bot.sendMessage(chat_id=chat_id, text="I'm back.", reply_markup=reply_markup)
```

#### [Download a file](https://core.telegram.org/bots/api#getfile)

```python
>>> file_id = message.voice.file_id
>>> newFile = bot.getFile(file_id)
>>> newFile.download('voice.ogg')
```

**Note:** For downloading photos, keep in mind that `update.message.photo` is an array of different photo sizes. Use `update.message.photo[-1]` to get the biggest size.

#### [Message entities](https://core.telegram.org/bots/api#messageentity)
To use MessageEntity, extract the entities from a Message object using `get_entities`.  

**Note:** This method should always be used instead of the ``entities`` attribute, since it calculates the correct substring from the message text based on UTF-16 codepoints - that is, it extracts the correct string even on when working with weird characters such as Emojis.

```python
>>> entities = message.get_entities()
```

There are many more API methods. To read the full API documentation, visit the [Telegram API documentation](https://core.telegram.org/bots/api) or the [library documentation of telegram.Bot](http://python-telegram-bot.readthedocs.io/en/latest/telegram.bot.html)

## Advanced snippets

#### Restrict access to a handler (decorator)

<!--- The extraction of the user_id is going to be built in on python-telegram-bot version 6.0.
TODO: Upon release, update this snippet!--->

This decorator allows you to restrict the access of a handler to only the `user_ids` specified in `LIST_OF_ADMINS`.

```python
from functools import wraps

LIST_OF_ADMINS = [12345678, 87654321]

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        # extract user_id from arbitrary update
        try:
            user_id = update.message.from_user.id
        except (NameError, AttributeError):
            try:
                user_id = update.inline_query.from_user.id
            except (NameError, AttributeError):
                try:
                    user_id = update.chosen_inline_result.from_user.id
                except (NameError, AttributeError):
                    try:
                        user_id = update.callback_query.from_user.id
                    except (NameError, AttributeError):
                        print("No user_id available in update.")
                        return
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(chat_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped
```

##### Usage

Add a `@restricted` decorator on top of your handler declaration:

```python
@restricted
def my_handler(bot, update):
    pass  # only accessible if `user_id` is in `LIST_OF_ADMINS`.
```

#### Cached Telegram group administrator check
If you want to limit certain bot functions to group administrators, you have to test if a user is an administrator in the group in question. This however requires an extra API request, which is why it can make sense to cache this information for a certain time, especially if your bot is very busy.

This snippet requires [this timeout-based cache decorator](http://code.activestate.com/recipes/325905-memoize-decorator-with-timeout/#c1). ([gist mirror](https://gist.github.com/jh0ker/56f5b4fb7d015b1b9e4c74d4a91d4568))

Save the decorator to a new file named `mwt.py` and add this line to your imports:
```python
from mwt import MWT
```

Then, add the following decorated function to your script. You can change the timeout as required.
```python
@MWT(timeout=60*60)
def get_admin_ids(bot, chat_id):
    """Returns a list of admin IDs for a given chat. Results are cached for 1 hour."""
    return [admin.user.id for admin in bot.getChatAdministrators(chat_id)]
```

You can then use the function like this:
```python
if update.message.from_user.id in get_admin_ids(bot, update.message.chat_id):
    # admin only
```

**Note:** Private chats are not covered by this snippet. Make sure you handle them.

#### Build a menu with Buttons

Often times you will find yourself in need for a menu with dynamic content. Use the following `build_menu` method to create a button layout with `n_cols` columns out of a list of `buttons`.

```python
def build_menu(buttons: List,
               n_cols: int,
               header_buttons: List = None,
               footer_buttons: List = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu
```

You can use the `header_buttons` and `footer_buttons` lists to put buttons in the first or last row respectively.

##### Usage

![Output](http://i.imgur.com/susvvR7.png)

```python
button_list = [
    InlineKeyboardButton("col 1", ...),
    InlineKeyboardButton("col 2", ...),
    InlineKeyboardButton("row 2", ...)
]
reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
bot.send_message(..., "A two-column menu", reply_markup=reply_markup)
```
This is especially useful if put inside a helper method like `get_data_buttons` to work on dynamic data and updating the menu according to user input.

Replace the `...` in above snippet by an appropriate argument, as indicated in the [InlineKeyboardButton documentation](https://python-telegram-bot.readthedocs.io/en/latest/telegram.inlinekeyboardbutton.html). If you want to use `KeyboardButtons`, use `ReplyKeyboardMarkup` instead of `InlineKeyboardMarkup`.

#### Simple way of restarting the bot

The following handler allows you to easily restart the bot. It goes without saying that you should protect this method from access by unauthorized users.

```python
import os
import time
import sys

def restart(bot, update):
    bot.sendMessage(update.message.chat_id, "Bot is restarting...")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)
```

You can trigger this handler with the `/r`-command within Telegram, once you have added it to the dispatcher: `dispatcher.add_handler(CommandHandler('r', restart))`

## What to read next?
If you haven't read the tutorial "[Extensions – Your first Bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-–-Your-first-Bot)" yet, you might want to do it now.