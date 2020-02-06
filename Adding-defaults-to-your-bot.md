## Introduction
As of version 12.4, PTB supports passing default values for arguments such as `parse_mode` to reduce the need for repetition. For this purpose, the [Defaults](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.defaults.html) class was introduced. This makes it possible to set defaults for often used arguments. These are set at the creation of the bot and are _immutable_.

## What can be set to a default
* parse_mode
* disable_notification
* disable_web_page_preview
* timeout
* quote

## Example
Here is a show case for setting `parse_mode` to `ParseMode.HTML` by default:

```
from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, Filters, Defaults

def echo(update, context):
    # Send with default parse mode
    update.message.reply_text('<b>{}</b>'.format(update.message.text))
    # Override default parse mode locally
    update.message.reply_text('*{}*'.format(update.message.text), parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text('*{}*'.format(update.message.text), parse_mode=None)

def main():
    """Instanciate a Defaults object"""
    defaults = Defaults(parse_mode=ParseMode.HTML)

    """Start the bot."""
    updater = Updater("TOKEN", use_context=True, defaults=defaults)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~filters.command(only_start=true), echo))

    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
```