## Introduction
As of version 12.4, PTB supports passing default values for arguments such as `parse_mode` to reduce the need for repetition. For this purpose, the [Defaults](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.defaults.html) class was introduced. This makes it possible to set defaults for often used arguments. These are set at the creation of the bot and are _immutable_.

## What can be set to a default
* `parse_mode`
* `disable_notification`
* `disable_web_page_preview`
* `allow_sending_without_reply`
* `timeout`
* `quote`
* `tzinfo`
* `run_async`

## Example
Here is a show case for setting `parse_mode` to `ParseMode.HTML` and `tzinfo` to `pytz.timezone('Europe/Berlin')` by default:

```python
import pytz
import datetime as dtm

from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, Filters, Defaults


def job(context):
    chat_id = context.job.context
    local_now = dtm.datetime.now(context.bot.defaults.tzinfo)
    utc_now = dtm.datetime.utcnow()
    text = 'Running job at {} in timezone {}, which equals {} UTC.'.format(
        local_now, context.bot.defaults.tzinfo, utc_now
    )
    context.bot.send_message(chat_id=chat_id, text=text)


def echo(update, context):
    # Send with default parse mode
    update.message.reply_text('<b>{}</b>'.format(update.message.text))
    # Override default parse mode locally
    update.message.reply_text('*{}*'.format(update.message.text), parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text('*{}*'.format(update.message.text), parse_mode=None)

    # Schedule job
    context.job_queue.run_once(job, dtm.datetime.now() + dtm.timedelta(seconds=1),
                               context=update.effective_chat.id)


def main():
    """Instantiate a Defaults object"""
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=pytz.timezone('Europe/Berlin'))

    """Start the bot."""
    updater = Updater("TOKEN", use_context=True, defaults=defaults)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on non command text message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

```