
### Can my Bot receive messages in a channel?

**No.** The Telegram Bot API has no way for a bot to receive messages in a channel. 
To prevent [two bots getting stuck in a loop replying to each other](https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots), bots can not receive any messages sent by other bots. In a channel, the source of a message is unknown - it could always be a bot.

### How to request for location and contact from user ?

```python
>>> location_keyboard = telegram.KeyboardButton(text="send_location", request_location=True)
>>> contact_keyboard  = telegram.KeyboardButton(text="send_location", request_contact=True)
>>> custom_keyboard = [[ location_keyboard, contact_keyboard ]]
>>> reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
>>> bot.sendMessage(chat_id=chat_id, text="Would mind to share location and contact with me ?", reply_markup=reply_markup)
```