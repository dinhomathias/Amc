This page can be read on its own to find the code snippet you need right now. 

It is also a follow-up to the page [[Introduction to the API|Introduction-to-the-API]]. If you come from there, you can leave your command line open and just try out a few of these snippets.

- [Pure API](#pure-api)
    + [Fetch updates](#fetch-updates)
    + [Fetch images sent to your Bot](#fetch-images-sent-to-your-bot)
    + [Reply to messages](#reply-to-messages)
- [General code snippets](#general-code-snippets)
    + [Post a text message](#post-a-text-message)
    + [Reply to a message](#reply-to-a-message)
    + [Send a chat action](#send-a-chat-action)
    + [Requesting location and contact from user](#requesting-location-and-contact-from-user)
  * [Message Formatting (bold, italic, code, ...)](#message-formatting-bold-italic-code-)
    + [Post a text message with Markdown formatting](#post-a-text-message-with-markdown-formatting)
    + [Post a text message with HTML formatting](#post-a-text-message-with-html-formatting)
    + [Message entities](#message-entities)
    + [Telegram formatting to BBCode](#telegram-formatting-to-bbcode)
  * [Working with files and media](#working-with-files-and-media)
    + [Posting files](#posting-files)
    + [Sending files via inline mode](#sending-files-via-inline-mode)
    + [Editing a file](#editing-a-file)
    + [Downloading a file](#downloading-a-file)
  * [Keyboard Menus](#keyboard-menus)
    + [Custom Keyboards](#custom-keyboards)
    + [Remove a custom keyboard](#remove-a-custom-keyboard)
  * [Other useful stuff](#other-useful-stuff)
    + [Generate flag emojis from country codes](#generate-flag-emojis-from-country-codes)
    + [Map a Slot Machine Dice value to the corresponding symbols](#map-a-slot-machine-dice-value-to-the-corresponding-symbols)
    + [Get the new members group message](#get-the-new-members-message)
    + [Exclude forwarded channel posts in discussion groups from MessageHandlers](#exclude-forwarded-channel-posts-in-discussion-groups-from-messagehandlers)
    + [Exclude messages from anonymous admins](#exclude-messages-from-anonymous-admins)
- [Advanced snippets](#advanced-snippets)
    + [Register a function as a command handler (decorator)](#register-a-function-as-a-command-handler-decorator)
      - [Usage](#usage)
    + [Restrict access to a handler (decorator)](#restrict-access-to-a-handler-decorator)
      - [Usage](#usage-1)
    + [Send action while handling command (decorator)](#send-action-while-handling-command-decorator)
      - [Usage](#usage-2)
    + [Build a menu with Buttons](#build-a-menu-with-buttons)
      - [Usage](#usage-3)
    + [Cached Telegram group administrator check](#cached-telegram-group-administrator-check)
    + [Simple way of restarting the bot](#simple-way-of-restarting-the-bot)
    + [Store ConversationHandler States](#store-conversationhandler-states)
    + [Save and load jobs using pickle](#save-and-load-jobs-using-pickle)
    + [Telegram web login widget](#verify-data-from-telegram-web-login-widget)
- [What to read next?](#what-to-read-next)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

## Pure API

#### Fetch updates
To fetch messages sent to your Bot, you can use the [getUpdates](https://core.telegram.org/bots/api#getupdates) API method.

**Note:** You don't have to use `get_updates` if you are writing your bot with the `telegram.ext` submodule, since `telegram.ext.Updater` takes care of fetching all updates for you. Read more about that [[here|Extensions-–-Your-first-Bot]].

```python
updates = await bot.get_updates()
print([u.message.text for u in updates])
```

---
#### Fetch images sent to your Bot

```python
updates = await bot.get_updates()
print([u.message.photo for u in updates if u.message.photo])
```

---
#### Reply to messages
You'll always need the `chat_id`

```python
chat_id = (await bot.get_updates())[-1].message.chat_id
```

---
## General code snippets
These snippets usually apply to both ways of fetching updates. If you're using `telegram.ext`, you can get the `chat_id` in your handler callback with `update.message.chat_id`.

**Note:** In general, you can send messages to users by passing their user id as the `chat_id`. 
If the bot has a chat with the user, it will send the message to that chat.

---
#### Post a text message
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendmessage)

```python
await bot.send_message(chat_id=chat_id, text="I'm sorry Dave I'm afraid I can't do that.")
```

**Note:** `send_message` method (as any of `send_*` methods of `Bot` class) returns the instance of `Message` class, so it can be used in code later.

---
#### Reply to a message

This is a shortcut to `bot.send_message` with same defaults. Read more about it [in the docs](http://python-telegram-bot.readthedocs.io/en/latest/telegram.html#telegram.Message.reply_text). 

```python
await update.message.reply_text("I'm sorry Dave I'm afraid I can't do that.")
```

**Note:** There are equivalents of this method for replying with photos, audio etc., and similar shortcuts exist throughout the library.

---
#### Send a chat action
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendchataction)
Use this to tell the user that something is happening on the bot's side:

```python
await bot.send_chat_action(chat_id=chat_id, action=telegram.constants.ChatAction.TYPING)
```
Alternatively, if you have several commands and don't want to repeat the above code snippet inside all commands, you can copy the snippet below and just decorate the callback functions with `@send_typing_action`.

```python
from functools import wraps
from telegram.constants import ChatAction

def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    async def command_func(update, context, *args, **kwargs):
        await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return await func(update, context,  *args, **kwargs)

    return command_func

@send_typing_action
async def my_handler(update, context):
    pass # Will send 'typing' action while processing the request.
```

---
#### Requesting location and contact from user

```python
location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
contact_keyboard = telegram.KeyboardButton(text="send_contact", request_contact=True)
custom_keyboard = [[ location_keyboard, contact_keyboard ]]
reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
await bot.send_message(chat_id=chat_id, 
...                  text="Would you mind sharing your location and contact with me?", 
...                  reply_markup=reply_markup)
```

To catch the incoming message with the location/contact, use `MessageHandler` with `filters.LOCATION` and `filters.CONTACT`, respectively.

---
### Message Formatting (bold, italic, code, ...)

Telegram supports some formatting options for text. All the details about what is supported can be found [here](https://core.telegram.org/bots/api#formatting-options). Please keep in mind that you will have to escape the special characters as detailed in the documentation. PTB also offers a [helper function](https://python-telegram-bot.readthedocs.io/en/stable/telegram.utils.helpers.html#telegram.utils.helpers.escape_markdown) for escaping of Markdown text. For escaping of HTML text, you can use [`html.escape`](https://docs.python.org/3/library/html.html?#html.escape) from the standard library.

You can format text with every API method/type that has a `parse_mode` parameter. In addition to editing your text as described in the link above, pass one of the parse modes available through [`telegram.constants.ParseMode`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.constants.html#telegram.constants.ParseMode) to the `parse_mode` parameter. Since the `5.0` update of the Bot API (version `13.1+` of PTB), you can alternatively pass a list of [`telegram.MessageEntities`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.messageentity.html) to the `entities` parameter.

*Note:* In the API 4.5 update, Telegram introduced MarkdownV2, which supports nested entities and needs other escaping than v1. Markdown V1 is referred as legacy mode by the official API docs, and you should prefer MarkdownV2. Make sure to also use `reply_markdown_v2` instead of `reply_markdown` etc.

#### Post a text message with Markdown formatting
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendmessage)

```python
await bot.send_message(chat_id=chat_id, 
                 text="*bold* _italic_ `fixed width font` [link](http://google.com)\.", 
                 parse_mode=telegram.constants.ParseMode.MARKDOWN_V2)
```

---
#### Post a text message with HTML formatting
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#sendmessage)

```python
await bot.send_message(chat_id=chat_id, 
                 text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', 
                 parse_mode=telegram.constants.ParseMode.HTML)
```

---
#### Message entities
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots/api#messageentity)
To use `MessageEntity`, extract the entities and their respective text from a `Message` object using [`parse_entities`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.message.html#telegram.Message.parse_entities).  

**Note:** This method should always be used instead of the ``entities`` attribute, since it calculates the correct substring from the message text based on UTF-16 codepoints - that is, it extracts the correct string even on when working with weird characters such as Emojis.

```python
entities = message.parse_entities()
```

---
#### Telegram formatting to BBCode
This is an example how to use entities to convert Telegram formatting to BBCode. In the current version it does *not* support nested entities.

Define parsing function:

<details><summary>Click to expand</summary><p>

```python
import sys

def parse_bbcode(message_text, entities, urled=False):
    """BBCode parsing function"""
    if message_text is None:
        return None

    if not sys.maxunicode == 0xffff:
        message_text = message_text.encode('utf-16-le')

    bbcode_text = ''
    last_offset = 0

    for entity, text in sorted(entities.items(), key=(lambda item: item[0].offset)):

        if entity.type == 'text_link':
            insert = '[url={}]{}[/url]'.format(entity.url, text)
        elif entity.type == 'mention':
            insert = '[url=https://t.me/{0}]{1}[/url]'.format(text.strip('@'),text)
        elif entity.type == 'url' and urled:
            insert = '[url={0}]{0}[/url]'.format(text)
        elif entity.type == 'bold':
            insert = '[b]' + text + '[/b]'
        elif entity.type == 'italic':
            insert = '[i]' + text + '[/i]'
        elif entity.type == 'underline':
            insert = '[u]' + text + '[/u]'
        elif entity.type == 'strikethrough':
            insert = '[s]' + text + '[/s]'
        elif entity.type == 'code':
            insert = '[code]' + text + '[/code]'
        elif entity.type == 'pre':
            insert = '[pre]' + text + '[/pre]'
        else:
            insert = text
        if sys.maxunicode == 0xffff:
            bbcode_text += message_text[last_offset:entity.offset] + insert
        else:
            bbcode_text += message_text[last_offset * 2:entity.offset * 2].decode('utf-16-le') + insert

        last_offset = entity.offset + entity.length

    if sys.maxunicode == 0xffff:
        bbcode_text += message_text[last_offset:]
    else:
        bbcode_text += message_text[last_offset * 2:].decode('utf-16-le')
    return bbcode_text

```

</p></details>


Call it with:
```python
entities = update.message.parse_entities()
bbcode = parse_bbcode(update.message.text, entities, urled=True)
```

...or for photo captions:
```python
entities = update.message.parse_caption_entities()
bbcode = parse_bbcode(caption, entities, urled=True)
```
`bbcode` will contain message/caption text formatted in BBCode. `urled` parameter determines if URLs in text are to be processed as links or left as text.

---
### Working with files and media

#### Posting files

If you want to send a file, e.g. send a photo with the bot, you have three options:

* Upload the file
* Send an HTTP-link that leads to the file
* Send a `file_id` of a file that has already been sent.

Note that not every method is supported everywhere (e.g. for thumbnails you can't pass a `file_id`). Make sure to check out the documentation of the corresponding bot method for details.

Please also check out the [official docs](https://core.telegram.org/bots/api#sending-files) on sending files.

Let's have a look at how sending a document can be done.

1. Uploading a file:

    ```python
    await bot.send_document(chat_id=chat_id, document=open('tests/test.png', 'rb'))
    ```

2. Sending an HTTP-link

    ```python
    await bot.send_document(chat_id=chat_id, document='https://python-telegram-bot.org/static/testfiles/telegram.gif'))
    ```

3. Sending by `file_id`:

    ```python
    await bot.send_document(chat_id=chat_id, document=file_id))
    ```
    
    Two further notes on this:
    
    1. Each bot has its own `file_ids`, i.e. you can't use a `file_id` from a different bot to send a photo
    2. How do you get a `file_id` of a photo you sent? Read it from the return value of `bot.send_document` (or any other `Message` object you get your hands on):
    
        ```python
        message = await bot.send_document(...)
        file_id = message.document.file_id
        ```
       
This pretty much works the same way for all the other `send_<media_type>` methods like `send_photo`, `send_video` etc. There is one exception, though: `send_media_group`. A call to `send_media_group` looks like this:

```python
await bot.send_media_group(chat_id=chat_id, media=[media_1, media_2, ...])
```

The items in the `media` list must be instances of `InputMediaAudio`, `InputMediaDocument`, `InputMediaPhoto` or `InputMediaVideo`. The media comes into play like so:

```python
media_1 = InputMediaDocument(media=open('tests/test.png', 'rb'), ...)
media_1 = InputMediaDocument(media='https://python-telegram-bot.org/static/testfiles/telegram.gif', ...)
media_1 = InputMediaDocument(media=file_id, ...)
```

Please check out the documentation of [`InputMediaAudio`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.inputmediaaudio.html), [`InputMediaDocument`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.inputmediadocument.html), [`InputMediaPhoto`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.inputmediaphoto.html#telegram.InputMediaPhoto) and [`InputMediaVideo`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.inputmediavideo.html#telegram.InputMediaVideo) for the details on required and optional arguments.

---
#### Sending files via inline mode

You may want to allow users to send media via your bots inline mode. This works a little bit different than posting media via `send_*`. Most notable, you can't upload files for inline mode! You must provide either an HTTP-URL or a `file_id`.

Let's stick to example of sending a document. Then you have to provide an `InlineQueryResult` to `bot.answer_inline_query` that represents that document and here are the two options:

1. HTTP-URL:

    ```python
    result = InlineQueryResultDocument(document_url='https://python-telegram-bot.org/static/testfiles/telegram.gif', ...)
    ```
   
2. `file_id`:

    ```python
    result = InlineQueryResultCachedDocument(document_file_id=file_id, ...)
    ```

The scheme `InlineQueryResult<media_type>` vs `InlineQueryResultCached<media_type>` is similar for the other media types.
Again, please check out the docs for details on required and optional arguments. 

---
#### Editing a file

When you have sent a file, you may want edit it. This works similarly as `send_media_group`, i.e. the media must be wrapped into a `InputMedia<media_type>` object. Again, with `document` as example:

```python
await bot.edit_message_media(chat_id=chat_id, message_id=message_id, media=InputMediaDocument(media=open('tests/test.png'), ...))
```

Please check out the restrictions on editing media in the docs of [`edit_message_media`](https://core.telegram.org/bots/api#editmessagemedia).

---
#### Downloading a file

When you receive files from a user, you sometimes want to download and save them. If it's a document, that could look like this:

```python
file_id = message.document.file_id
newFile = await bot.get_file(file_id)
await newFile.download()
```

For a received video/voice/... change `message.document` to `message.video/voice/...`. However, there is one exception: `message.photo` is a *list* of `PhotoSize` objects, which represent different sizes of the same photo. Use `message.photo[-1].file_id` to get the largest size.

Moreover, the above snippet can be shortened by using PTBs built-in utility shortcuts:

```python
newFile = await message.effective_attachment.get_file()
await newFile.download('file_name')
```

`message.effective_attachment` automatically contains whichever media attachment the message has - in case of a photo, you'll again have to use e.g. `message.effective_attachment[-1].get_file()`

---
### Keyboard Menus

#### Custom Keyboards
[ᵀᴱᴸᴱᴳᴿᴬᴹ](https://core.telegram.org/bots#keyboards)

```python
custom_keyboard = [['top-left', 'top-right'], 
                   ['bottom-left', 'bottom-right']]
reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
await bot.send_message(
    chat_id=chat_id, 
    text="Custom Keyboard Test", 
    reply_markup=reply_markup
)
```

See also: [Build a menu with Buttons](#build-a-menu-with-buttons)


---
#### Remove a custom keyboard

```python
reply_markup = telegram.ReplyKeyboardRemove()
await bot.send_message(
    chat_id=chat_id, text="I'm back.", reply_markup=reply_markup
)
```

---
### Other useful stuff

#### Generate flag emojis from country codes

The Unicode flag emoji for any country can by definition be calculated from the countries [2 letter country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2). The following snippet only works in Python 3.

```python
OFFSET = 127462 - ord('A')

def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)

>>> flag('un')
'🇺🇳'
>>> flag('eu')
'🇪🇺'
```

---
#### Map a Slot Machine Dice value to the corresponding symbols

The 🎰 dice can take the values 1-64. Here is a dictionary that maps each value to the unique combination of symbols that produce that value:

(Source: This [Gist](https://gist.github.com/Chase22/300bad79154ffd5d8fbf0aedd5ddc4d4) by [@Chase22](https://github.com/Chase22))

<details><summary>Click to expand</summary><p>

```python
slot_machine_value = {
    1: ("bar", "bar", "bar"),
    2: ("grape", "bar", "bar"),
    3: ("lemon", "bar", "bar"),
    4: ("seven", "bar", "bar"),
    5: ("bar", "grape", "bar"),
    6: ("grape", "grape", "bar"),
    7: ("lemon", "grape", "bar"),
    8: ("seven", "grape", "bar"),
    9: ("bar", "lemon", "bar"),
    10: ("grape", "lemon", "bar"),
    11: ("lemon", "lemon", "bar"),
    12: ("seven", "lemon", "bar"),
    13: ("bar", "seven", "bar"),
    14: ("grape", "seven", "bar"),
    15: ("lemon", "seven", "bar"),
    16: ("seven", "seven", "bar"),
    17: ("bar", "bar", "grape"),
    18: ("grape", "bar", "grape"),
    19: ("lemon", "bar", "grape"),
    20: ("seven", "bar", "grape"),
    21: ("bar", "grape", "grape"),
    22: ("grape", "grape", "grape"),
    23: ("lemon", "grape", "grape"),
    24: ("seven", "grape", "grape"),
    25: ("bar", "lemon", "grape"),
    26: ("grape", "lemon", "grape"),
    27: ("lemon", "lemon", "grape"),
    28: ("seven", "lemon", "grape"),
    29: ("bar", "seven", "grape"),
    30: ("grape", "seven", "grape"),
    31: ("lemon", "seven", "grape"),
    32: ("seven", "seven", "grape"),
    33: ("bar", "bar", "lemon"),
    34: ("grape", "bar", "lemon"),
    35: ("lemon", "bar", "lemon"),
    36: ("seven", "bar", "lemon"),
    37: ("bar", "grape", "lemon"),
    38: ("grape", "grape", "lemon"),
    39: ("lemon", "grape", "lemon"),
    40: ("seven", "grape", "lemon"),
    41: ("bar", "lemon", "lemon"),
    42: ("grape", "lemon", "lemon"),
    43: ("lemon", "lemon", "lemon"),
    44: ("seven", "lemon", "lemon"),
    45: ("bar", "seven", "lemon"),
    46: ("grape", "seven", "lemon"),
    47: ("lemon", "seven", "lemon"),
    48: ("seven", "seven", "lemon"),
    49: ("bar", "bar", "seven"),
    50: ("grape", "bar", "seven"),
    51: ("lemon", "bar", "seven"),
    52: ("seven", "bar", "seven"),
    53: ("bar", "grape", "seven"),
    54: ("grape", "grape", "seven"),
    55: ("lemon", "grape", "seven"),
    56: ("seven", "grape", "seven"),
    57: ("bar", "lemon", "seven"),
    58: ("grape", "lemon", "seven"),
    59: ("lemon", "lemon", "seven"),
    60: ("seven", "lemon", "seven"),
    61: ("bar", "seven", "seven"),
    62: ("grape", "seven", "seven"),
    63: ("lemon", "seven", "seven"),
    64: ("seven", "seven", "seven"),
}
```

</p></details>

---
#### Get the new members message
```python
import asyncio

async def add_group(update: Update, context: CallbackContext):
    await asyncio.gather(
        update.message.reply_text(f"{member.full_name} just joined the group")
        for member in update.message.new_chat_members
    )

add_group_handle = MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, add_group)
application.add_handler(add_group_handle)
```
Note that service messages about non-bot users joining the chat are removed from large groups. You can get the new members message by following the [chatmemberbot.py example](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples#chatmemberbotpy).

---
#### Exclude forwarded channel posts in discussion groups from MessageHandlers	
If you're using `MessageHandlers` and do not want them to respond to the channel posts automatically forwarded to the discussion group linked to your channel, you can use this filter in your `MessageHandler` (requires PTB v13.9+):
```python	
~ filters.IS_AUTOMATIC_FORWARD 
```

---
#### Exclude Messages from anonymous Admins	
If you're using `MessageHandlers` and do not want them to respond to messages from anonymous admins, you can use this filter in your `MessageHandler`:
```python	
~ filters.SenderChat.SUPER_GROUP
```

---
## Advanced snippets

#### Register a function as a command handler (decorator)

This decorator allows you to register a function as a command handler in a _Flask_ like manner.

```python
def command_handler(command):
    def decorator(func):
        handler = CommandHandler(command, func)
        application.add_handler(handler)
        return func
    return decorator
```

##### Usage

Add the `@command_handler(command)` decorator on top of your handler function:

```python
@command_handler("hello")
async def hello(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello world!")
```

**Note**: You can modify this decorator in order to register any type of handler (see [[Types Of Handlers|Types-Of-Handlers]]). Please also note that PTB deliberately does not provide such functionality out of the box due to the reasons mentioned in [#899](https://github.com/python-telegram-bot/python-telegram-bot/issues/899).

---
#### Restrict access to a handler (decorator)

This decorator allows you to restrict the access of a handler to only the `user_ids` specified in `LIST_OF_ADMINS`.

```python
from functools import wraps

LIST_OF_ADMINS = [12345678, 87654321]

def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print(f"Unauthorized access denied for {user_id}.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped
```

##### Usage

Add a `@restricted` decorator on top of your handler declaration:

```python
@restricted
async def my_handler(update, context):
    pass  # only accessible if `user_id` is in `LIST_OF_ADMINS`.
```

---
#### Send action while handling command (decorator)
This parametrized decorator allows you to signal different actions depending on the type of response of your bot. This way users will have similar feedback from your bot as they would from a real human. 
```python
from functools import wraps

def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        async def command_func(update, context, *args, **kwargs):
            await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return await func(update, context,  *args, **kwargs)
        return command_func
    
    return decorator
```

##### Usage
![Result](https://i.imgur.com/ErBKSS4.png)

You can decorate handler callbacks directly with `@send_action(ChatAction.<Action>)` or create aliases and decorate with them (more readable) .
```python
send_typing_action = send_action(ChatAction.TYPING)
send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)
```
With the above aliases, the following decorators are equivalent
```python
@send_typing_action
async def my_handler(update, context):
    pass  # user will see 'typing' while your bot is handling the request.
    
@send_action(ChatAction.TYPING)
async def my_handler(update, context):
    pass  # user will see 'typing' while your bot is handling the request.
```
All possible actions are documented [here](https://core.telegram.org/bots/api#sendchataction).

---
#### Build a menu with Buttons

Often times you will find yourself in need for a menu with dynamic content. Use the following `build_menu` method to create a button layout with `n_cols` columns out of a list of `buttons`.

```python
from typing import Union, List
from telegram import InlineKeyboardButton

def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu
```

You can use the `header_buttons` and `footer_buttons` lists to put buttons in the first or last row respectively.

##### Usage

![Output](http://i.imgur.com/susvvR7.png)

Replace the `...` in below snippet by an appropriate argument, as indicated in the [InlineKeyboardButton documentation](https://python-telegram-bot.readthedocs.io/en/latest/telegram.inlinekeyboardbutton.html). If you want to use `KeyboardButtons`, use `ReplyKeyboardMarkup` instead of `InlineKeyboardMarkup`.

```python
button_list = [
    InlineKeyboardButton("col1", callback_data=...),
    InlineKeyboardButton("col2", callback_data=...),
    InlineKeyboardButton("row 2", callback_data=...)
]
reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
await bot.send_message(..., "A two-column menu", reply_markup=reply_markup)
```

Or, if you need a dynamic version, use list comprehension to generate your `button_list` dynamically from a list of strings:

```python
some_strings = ["col1", "col2", "row2"]
button_list = [[KeyboardButton(s)] for s in some_strings]
```

This is especially useful if put inside a helper method like `get_data_buttons` to work on dynamic data and updating the menu according to user input.

To handle the `callback_data`, you need to set a `CallbackQueryHandler`.

#### Verify data from [Telegram Web Login Widget](https://core.telegram.org/widgets/login). 

When using a [`LoginUrl`](https://core.telegram.org/bots/api#loginurl) in an [`InlineKeyboardButton`](https://core.telegram.org/bots/api#inlinekeyboardbutton) to authorize a user on your website via Telegram, you'll have to to check the hash of the received data to verify the data of the integrity as described [here](https://core.telegram.org/widgets/login#checking-authorization)

The data JSON data will have the following form:
```python
{
    "id": XXXXXXXXX
    "first_name": "XXX"
    "last_name": "XXX"
    "username": "XXXXX"
    "photo_url": "https://t.meXXXXXX.jpg"
    "auth_date": XXXXXXXXXX
    "hash": "XXXXXXXXXXXXXXXXXXXXXX....."
}
 ```    
The following is an example implementation in Python:

<details><summary>Click to expand</summary><p>

```python
import hashlib
import hmac

BOT_TOKEN = 'YOUR BOT TOKEN'

def verify(request_data):
    request_data = request_data.copy()
    tg_hash = request_data['hash']
    request_data.pop('hash', None)
    request_data_alphabetical_order = sorted(request_data.items(), key=lambda x: x[0])

    data_check_string = []
    for data_pair in request_data_alphabetical_order:
        key, value = data_pair[0], data_pair[1]
        data_check_string.append(f"{key}={value}")
    data_check_string = '\n'.join(data_check_string)

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    received_hash = hmac.new(secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256).hexdigest()

    if received_hash == tg_hash:
        # The user clicked to the Auth Button and data is verified.
        print('User Logged in.')
        return True
    else:
        # The data is not valid
        print('User data mis-matched.')
        return False

    # Optionally use another if-else block to check the auth_date in order to prevent outdated data from being verified.
```

</p></details>

A sample of Flask app can be found [here.](https://gist.github.com/jainamoswal/279e5259a5c24f37cd44ea446c373ac4)