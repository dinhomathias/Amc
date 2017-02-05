This page can be read on its own to find the code snippet you need right now. 

It is also a follow-up to the page [Introduction to the API](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API). If you come from there, you can leave your command line open and just try out a few of these snippets.


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


#### Post a text message

```python
>>> bot.sendMessage(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")
```

#### Reply to a message

This is a shortcut to `bot.sendMessage` with sane defaults. Read more about it [in the docs](http://python-telegram-bot.readthedocs.io/en/latest/telegram.html#telegram.Message.reply_text). 

```python
>>> update.message.reply_text("I'm sorry Dave I'm afraid I can't do that.")
```

**Note:** There are equivalents of this method for replying with photos, audio etc., and similar shortcuts exist throughout the library. Related PRs: [#362](https://github.com/python-telegram-bot/python-telegram-bot/pull/362), [#420](https://github.com/python-telegram-bot/python-telegram-bot/pull/420), [#423](https://github.com/python-telegram-bot/python-telegram-bot/pull/423)

#### Post a text message with Markdown formatting

```python
>>> bot.sendMessage(chat_id=chat_id, 
...                 text="*bold* _italic_ `fixed width font` [link](http://google.com).", 
...                 parse_mode=telegram.ParseMode.MARKDOWN)
```

#### Post a text message with HTML formatting

```python
>>> bot.sendMessage(chat_id=chat_id, 
...                 text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', 
...                 parse_mode=telegram.ParseMode.HTML)
```

#### Post an image file from disk

```python
>>> bot.sendPhoto(chat_id=chat_id, photo=open('tests/test.png', 'rb'))
```

#### Post a voice file from disk

```python
>>> bot.sendVoice(chat_id=chat_id, voice=open('tests/telegram.ogg', 'rb'))
```

#### Post a file from an URL

```python
>>> bot.sendPhoto(chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')
```

#### Send a chat action
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

#### Download a file

```python
>>> file_id = message.voice.file_id
>>> newFile = bot.getFile(file_id)
>>> newFile.download('voice.ogg')
```

**Note:** For downloading photos, keep in mind that `update.message.photo` is an array of different photo sizes. Use `update.message.photo[-1]` to get the biggest size.

#### Message entities
To use MessageEntity, extract the entities from a Message object using `get_entities`.  

**Note:** This method should always be used instead of the ``entities`` attribute, since it calculates the correct substring from the message text based on UTF-16 codepoints - that is, it extracts the correct string even on when working with weird characters such as Emojis.

```python
>>> entities = message.get_entities()
```

There are many more API methods. To read the full API documentation, visit the [Telegram API documentation](https://core.telegram.org/bots/api) or the [library documentation of telegram.Bot](http://python-telegram-bot.readthedocs.io/en/latest/telegram.bot.html)

## Advanced snippets

#### Cached administrator check
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

```
def build_menu(buttons: List,
               n_cols: int,
               header_buttons: List = None,
               footer_buttons: List = None):
    menu = list()
    for i in range(0, len(buttons)):
        item = buttons[i]
        if i % n_cols == 0:
            menu.append([item])
        else:
            menu[int(i / n_cols)].append(item)
    if header_buttons:
        menu.insert(0, header_buttons)
    if header_buttons:
        menu.append(footer_buttons)
    return menu
```

You can use the `header_buttons` and `footer_buttons` lists to put buttons in the first or last row respectively.

##### Usage

![Output](http://i.imgur.com/susvvR7.png)

```
button_list = [
    InlineKeyboardButton("col 1", ...),
    InlineKeyboardButton("col 2", ...),
    InlineKeyboardButton("row 2", ...)
]
reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
bot.send_message(..., "A two-column menu", reply_markup=reply_markup)
```
This is especially useful if put inside a helper method like `get_data_buttons` to work on dynamic data and updating the menu according to user input.

## What to read next?
If you haven't read the tutorial "[Extensions – Your first Bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-–-Your-first-Bot)" yet, you might want to do it now.