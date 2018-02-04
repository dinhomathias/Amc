This page describes advanced use cases for the filters used with `MessageHandler` from `telegram.ext`.

## Combining filters
When using `MessageHandler` it is sometimes useful to have more than one filter. This can be done using so called bit-wise operators. In python those operators are `&`, `|` and `~` meaning AND, OR and NOT respectively.
### Examples
#### Message is either video, photo, or document (generic file)
``` python
from telegram.ext import MessageHandler, Filters

handler = MessageHandler(Filters.video | Filters.photo | Filters.document, 
                         callback)
```

#### Message is a forwarded photo
``` python
handler = MessageHandler(Filters.forwarded & Filters.photo, callback)
```

#### Message is text and contains a link
``` python
from telegram import MessageEntity

handler = MessageHandler(
    Filters.text & (Filters.entity(MessageEntity.URL) |
                    Filters.entity(MessageEntity.TEXT_LINK)),
    callback)
```

#### Message is a photo and it's not forwarded
``` python
handler = MessageHandler(Filters.photo & (~ Filters.forwarded), callback)
```

## Custom filters
It is also possible to write our own filters. In essence, a filter is simply a function that receives a `Message` instance and returns either `True` or `False`. This function has to be implemented in a new class that inherits from `BaseFilter`, which allows it to be combined with other filters. If the combination of all filters evaluates to `True`, the message will be handled. 

Say we wanted to allow only those messages that contain the text "python-telegram-bot is awesome", we could write a custom filter as so:

```python
from telegram.ext import BaseFilter

class FilterAwesome(BaseFilter):
    def filter(self, message):
        return 'python-telegram-bot is awesome' in message.text

# Remember to initialize the class.
filter_awesome = FilterAwesome()
```

The class can of cause be named however you want, the only important things are:
- The class has to inherit from `BaseFilter`
- It has to implement a `filter` method
- You have to create an instance of the class

The filter can then be used as:
```python
awesome_handler = MessageHandler(filter_awesome, callback)
```