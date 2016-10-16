This page describes advanced use cases for the filters used with `MessageHandler` from `telegram.ext`.

## Combining filters
When using `MessageHandler` it is sometimes useful to have more than one filter. This can be done using so called bit-wise operators. In python those operators are `&` and `|` meaning AND and OR respectively.
### Examples
#### Message is either video, photo, or document (generic file)
``` python
awesome_handler = MessageHandler(Filters.video | Filters.photo | Filters.document, link_function)
```

#### Message is a forwarded photo
``` python
awesome_handler = MessageHandler(Filters.forwarded & Filters.photo, link_function)
```

#### Message is text and contains a link
``` python
awesome_handler = MessageHandler(Filters.text & (Filters.entity(URL) | Filters.entity(TEXT_LINK)), link_function)
```

## Custom filters
It is also possible to write our own filters. In essence a filter is actually just a python function, that receives a message and returns either `True` if the message should be filtered. However, since we want to be able to combine (see above) multiple filters, we have to define them a bit differently (namely write a class and inherit from `BaseFilter`.

Say we wanted to only filter messages that includes text like "python-telegram-bot is awesome" we could write a custom filter as so:

``` python
class filter_awesome(BaseFilter):
    def fitler(messsage):
        if 'python-telegram-bot is awesome' in message.text:
            return True
```

The class could of cause be named whatever you want, the only important things to take note of is that the class *must* inherit from BaseFilter and also implement a `filter` method.

The filter could then be used as:
``` python
awesome_handler = MessageHandler(filter_awesome, awesome_function)
```