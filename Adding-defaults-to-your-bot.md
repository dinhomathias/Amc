## Introduction
As of version 12.4, PTB supports passing default values for arguments such as `parse_mode` to reduce the need for repetition. For this purpose, the [Defaults](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.defaults.html) class was introduced. This makes it possible to set defaults for often used arguments. These are set at the creation of the bot and are _immutable_.

## What can be set to a default
* `parse_mode`
* `disable_notification`
* `disable_web_page_preview`
* `allow_sending_without_reply`
* `quote`
* `tzinfo`
* `block`
* `protect_content`

## Example
Here is a show case for setting `parse_mode` to `ParseMode.HTML` and `tzinfo` to `pytz.timezone('Europe/Berlin')` by default:

```python
import logging

import pytz
import datetime as dtm

from telegram.constants import ParseMode
from telegram.ext import MessageHandler, filters, Defaults, Application

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


async def job(context):
    chat_id = context.job.chat_id
    timezone = context.bot.defaults.tzinfo
    local_now = dtm.datetime.now(timezone)
    utc_now = dtm.datetime.utcnow()
    text = f'Running job at {local_now} in timezone {timezone}, which equals {utc_now} UTC.'
    await context.bot.send_message(chat_id=chat_id, text=text)


async def echo(update, context):
    text = update.message.text
    # Send with default parse mode
    await update.message.reply_text(f'<b>{text}</b>')
    # Override default parse mode locally
    await update.message.reply_text(f'*{text}*', parse_mode=ParseMode.MARKDOWN)
    # Send with no parse mode
    await update.message.reply_text(f'*{text}*', parse_mode=None)

    # Schedule job
    context.job_queue.run_once(
        job, dtm.datetime.now() + dtm.timedelta(seconds=1), chat_id=update.effective_chat.id
    )


def main():
    """Instantiate a Defaults object"""
    defaults = Defaults(parse_mode=ParseMode.HTML, tzinfo=pytz.timezone('Europe/Berlin'))

    application = (
        Application.builder()
        .token("TOKEN")
        .defaults(defaults)
        .build()
    )

    # on non command text message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the Bot
    application.run_polling()


if __name__ == '__main__':
    main()

```