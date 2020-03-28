# Introduction
Hey, this wiki page will walk you through the inline keyboard example found [here](../blob/master/examples/inlinekeyboard.py). We will start with how python starts with the example, then follow through the code in the same way we expect updates from the user would go through it. Let's do it.

_Disclaimer: We will conveniently ignore the imports._
## Startup

```python
if __name__ == '__main__':
    main()
```
[Lines 63 to 64](../blob/master/examples/inlinekeyboard.py#L63-L64) tell python that after starting the script, it's supposed to call the main function
## main

```python
updater = Updater("TOKEN", use_context=True)
```
[First line](../blob/master/examples/inlinekeyboard.py#L48) in the main function, it creates an updater instance from the [Updater class](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.updater.html). The "TOKEN" part is where you put the bot token, use_context means that we use context based handlers.

```python
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_error_handler(error)
```
[Line 50 to 53](../blob/master/examples/inlinekeyboard.py#L50-53) registers our four handlers. The first handler is a [CommandHandler](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.commandhandler.html). Whenever an user sends a /start command to the bot, the function `start` is called. Same situation with the third handler: Whenever an user sends the /help command, `help` gets called.

The second handler is a [CallbackQueryHandler](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.callbackqueryhandler.html). A [Callbackquery](https://python-telegram-bot.readthedocs.io/en/stable/telegram.callbackquery.html) is what an user sends after he presses an [InlineButton](https://python-telegram-bot.readthedocs.io/en/stable/telegram.inlinekeyboardbutton.html). Every press of a button gets send to the `button` handler.

The last handler is an [error handler](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.dispatcher.html#telegram.ext.Dispatcher.add_error_handler). Every error which was raised after an update, wherever it happens in this code, will get send to the `error` handler and can be dealt with there.

```python
updater.start_polling()
```
[Line 56](../blob/master/examples/inlinekeyboard.py#L56) tells the PTB library to start the bot using polling, which means that the library will continuously make a request to the telegram servers and get new updates from there, if they exists.

```python
updater.idle()
```
[Line 60](../blob/master/examples/inlinekeyboard.py#L60) actually runs the bot until a termination signal is send.


Let's start our way through the handlers in the same way we would expect an user to go through it: With the start handler:
## start

```python
def start(update, context):
```
[Line 18](../blob/master/examples/inlinekeyboard.py#L18) we define a function called start. It takes the two arguments update (instance of an [Update](https://python-telegram-bot.readthedocs.io/en/stable/telegram.update.html)) and context (instance of a [CallbackContext](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.callbackcontext.html)).

```python
keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
             InlineKeyboardButton("Option 2", callback_data='2')],

          [InlineKeyboardButton("Option 3", callback_data='3')]]

```
[Line 19 to 22](../blob/master/examples/inlinekeyboard.py#L19-L22) a variable called keyboard is defined. It is a double list. Every entry in the first list is a row in the actual inline keyboard, every entry in the list entry is a column. So this keyboard will have two rows, Option 1 and Option 2 will be in the first; Option 3 in the second one.

```python
reply_markup = InlineKeyboardMarkup(keyboard)
```
[Line 24](../blob/master/examples/inlinekeyboard.py#L24) turns our list into an actual Inline Keyboard that we can pass along with our message.

```python
update.message.reply_text('Please choose:', reply_markup=reply_markup)
```
[Line 26](../blob/master/examples/inlinekeyboard.py#L26) we reply to the update message with a text (hence [reply_text](https://python-telegram-bot.readthedocs.io/en/stable/telegram.message.html#telegram.Message.reply_text)) and pass the keyboard along in the reply_markup argument.

Now we expect people to press one of the provided buttons, so let's jump to the button callback
## button

```python
def button(update, context):
```
[Line 29](../blob/master/examples/inlinekeyboard.py#L29) we define a function called button. It takes the two arguments update and context.

```python
query = update.callback_query

query.edit_message_text(text="Selected option: {}".format(query.data))
```
[Line 30 to 32](../blob/master/examples/inlinekeyboard.py#L30-L32) query is defined as a shortcut to access the provided callbackquery. Then we edit the message where to callbackquery originates from with the text where we tell the user which option we picked. We insert `query.data` into the string, which is the data we defined in the keyboard, so the number 1, 2 or 3. Since we don't pass the inline keyboard along again, it will disappear.
## help

```python
def help(update, context):
    update.message.reply_text("Use /start to test this bot.")
```
[Line 35 to 36](../blob/master/examples/inlinekeyboard.py#L35-L36) in this simple callback, we reply to the /help command with the provided text, that they should use /start to use this bot.
## error

```python
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
```
[Line 39 to 41](../blob/master/examples/inlinekeyboard.py#L39-41) we simply log in the logger that the provided update raised the provided error.

***

This section of the wiki is currently in development, feedback is greatly appreciated. Ping one of the admins in our telegram group to anything you want to tell us.