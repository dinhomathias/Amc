# Introduction
Hey, this wiki page will walk you through the inline keyboard example found [here](../blob/master/examples/inlinekeyboard.py). We will start with how python starts with the example, then follow through the code in the same way we expect updates from the user would go through it. Let's do it.

_Disclaimer: We will conveniently ignore the imports._
## Startup

```python
if __name__ == '__main__':
    main()
```
[Lines 68 to 69](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L68-L69) tell python that after starting the script, it's supposed to call the main function
## main

```python
updater = Updater("TOKEN")
```
[The first line](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L54) in the main function, it creates an updater instance from the [Updater class](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.updater.html). The "TOKEN" part is where you put the bot token.

```python
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help_command))
```
[Line 56 to 58](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L56-L58) registers our three handlers. The first handler is a [CommandHandler](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.commandhandler.html). Whenever an user sends a /start command to the bot, the function `start` is called. Same situation with the third handler: Whenever an user sends the /help command, `help_command` gets called.

The second handler is a [CallbackQueryHandler](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.callbackqueryhandler.html). A [Callbackquery](https://python-telegram-bot.readthedocs.io/en/stable/telegram.callbackquery.html) is what an user sends after he presses an [InlineButton](https://python-telegram-bot.readthedocs.io/en/stable/telegram.inlinekeyboardbutton.html). Every press of a button gets send to the `button` handler.

```python
updater.start_polling()
```
[Line 61](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L61) tells the PTB library to start the bot using polling, which means that the library will continuously make a request to the telegram servers and get new updates from there, if they exists.

```python
updater.idle()
```
[Line 65](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L65) actually runs the bot until a termination signal is send.


Let's start our way through the handlers in the same way we would expect an user to go through it: With the start handler:
## start

```python
def start(update: Update, context: CallbackContext) -> None:
```
[Line 20](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L20) we define a function called start. It takes the two arguments update (instance of an [Update](https://python-telegram-bot.readthedocs.io/en/stable/telegram.update.html)) and context (instance of a [CallbackContext](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.callbackcontext.html)). The `->` indicates to a type checker that this function returns nothing.

```python
keyboard = [
    [
        InlineKeyboardButton("Option 1", callback_data='1'),
        InlineKeyboardButton("Option 2", callback_data='2'),
    ],
    [InlineKeyboardButton("Option 3", callback_data='3')],
]

```
[Line 22 to 28](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L22-L28) a variable called keyboard is defined. It is a double list. Every entry in the first list is a row in the actual inline keyboard, every entry in the list entry is a column. So this keyboard will have two rows, Option 1 and Option 2 will be in the first; Option 3 in the second one.

```python
reply_markup = InlineKeyboardMarkup(keyboard)
```
[Line 30](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L30) turns our list into an actual Inline Keyboard that we can pass along with our message.

```python
update.message.reply_text('Please choose:', reply_markup=reply_markup)
```
[Line 32](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L32) we reply to the update message with a text (hence [reply_text](https://python-telegram-bot.readthedocs.io/en/stable/telegram.message.html#telegram.Message.reply_text)) and pass the keyboard along in the `reply_markup` argument.

Now we expect people to press one of the provided buttons, so let's jump to the button callback
## button

```python
def button(update: Update, context: CallbackContext) -> None:
```
[Line 35](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L35) we define a function called button. It takes the two arguments update and context, basically the same as `start`.

```python
query = update.callback_query
```
[Line 37](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L37) query is defined as a shortcut to access the provided [CallbackQuery](https://python-telegram-bot.readthedocs.io/en/stable/telegram.callbackquery.html). This is the part of the update which has all the information in it, remember, it gets generated/send to the bot once a user presses a button.


```python
query.answer()
```
[Line 41](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L41) here we answer the `CallbackQuery`. We use a convenient shortcut PTB provides. It takes care of calling the [actual function](https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html#telegram.Bot.answer_callback_query) and passing all the required parameters to it. If you check out the function, you see that you can pass a `text` argument to it, which will be displayed in a little pop-up on the client end, and if you pass `show_alert` on top of it, the user has to dismiss the pop-up. Not useful for this example, so we just pass it without these optional arguments.

```python
query.edit_message_text(text=f"Selected option: {query.data}")
```
[Line 43](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L43) then we edit the message where `CallbackQuery` originates from with the text where we tell the user which option we picked. We insert `query.data` into the string, which is the data we defined in the keyboard, so the number 1, 2 or 3. Since we don't pass the inline keyboard along again, it will disappear.
## help

```python
def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Use /start to test this bot.")
```
[Line 46 to 48](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L46-L48) in this simple callback, we reply to the /help command with the provided text, that they should use /start to use this bot.
## error

```python
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
```
[Line 14 to 17](https://github.com/python-telegram-bot/python-telegram-bot/blob/92cb6f3ae8d5c3e49b9019a9348d4408135ffc95/examples/inlinekeyboard.py#L14-L17) are the only lines of the code we haven't covered yet. Here we set up the logging module to have the format we want, and we define logger in case we want to use it later. More docs regarding logging can be found [here](https://docs.python.org/3/library/logging.html)

***

This section of the wiki is currently in development, feedback is greatly appreciated. Ping one of the admins in our telegram group to anything you want to tell us.