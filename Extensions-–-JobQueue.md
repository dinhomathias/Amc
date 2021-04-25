# Introduction
The extension class `telegram.ext.JobQueue` allows you to perform tasks with a delay or even periodically, at a set interval. Among many other things, you can use it to send regular updates to your subscribers.

## When working with `JobQueue`, please keep in mind:

* PTBs `JobQueue` provides an easy to use and ready to use way of scheduling tasks in a way that ties in with the PTB architecture
* Managing scheduling logic is not the main intend of PTB and hence as of v13 a third party library is used
* If you need highly customized scheduling thingies, you *can* use advanced features of the third party library
* We can't guarantee that the backend will stay the same forever. For example, if the third party library is discontinued, we will have to look for alternatives.

## Example

In addition to the tutorial below there is also the `timerbot.py` example at the [examples directory](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples).

# Usage
The `JobQueue` class is tightly integrated with other `telegram.ext` classes. Similar to `Updater` and `Dispatcher`, it runs asynchronously in a separate thread.

To use the `JobQueue`, you don't have to do much. When you instantiate the `Updater`, it will create a `JobQueue` for you:

```python
from telegram.ext import Updater

u = Updater('TOKEN', use_context=True)
j = u.job_queue
```

This job queue is also linked to the dispatcher, which is discussed later in this article. Just know that unless you have a good reason to do so, you should not instantiate `JobQueue` yourself.

Tasks in the job queue are encapsulated by the `Job` class. It takes a callback function as a parameter, which will be executed when the time comes. This callback function always takes one parameter: `context`, a `telegram.ext.CallbackContext`. Like in the case of handler callbacks used by the `Dispatcher`, through this object you can access `context.bot`, the `Updater`'s `telegram.Bot` instance; and for this particular case you can also access `context.job`, which is the `Job` instance of the task that triggered the callback (more on that later). 

You can use the following methods to create jobs with different frequency and time: `job_queue.run_once`, `job_queue.run_repeating`, `job_queue.run_daily` and `job_queue.run_monthly`. (As before, you do not usually need to instantiate the `Job` class directly.)

## Tutorial

Add your first job to the queue by defining a callback function and adding it to the job queue. For this tutorial, you can replace `'@examplechannel'` with a channel where your bot is an admin, or by your user id (use [@userinfobot](https://telegram.me/userinfobot) to find out your user id):

```python
def callback_minute(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id='@examplechannel', 
                             text='One message every minute')

job_minute = j.run_repeating(callback_minute, interval=60, first=10)
```

The `callback_minute` function will be executed every `60.0` seconds, the first time being after 10 seconds (because of `first=10`). The `interval` and `first` parameters are in seconds if they are `int` or `float`. They can also be `datetime` objects. See the [docs](http://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.jobqueue.html) for detailed explanation.
The return value of these functions are the `Job` objects being created. You don't need to store the result of `run_repeating` (which is the newly instantiated `Job`) if you don't need it; we will make use of it later in this tutorial.

You can also add a job that will be executed only once, with a delay:

```python
def callback_30(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id='@examplechannel', 
                             text='A single message with 30s delay')

j.run_once(callback_30, 30)
```

In thirty seconds you should receive the message from `callback_30`. 

If you are tired of receiving a message every minute, you can temporarily disable a job or even completely remove it from the queue:

```python
job_minute.enabled = False  # Temporarily disable this job
job_minute.schedule_removal()  # Remove this job completely
```

**Note:** `schedule_removal` does not immediately remove the job from the queue. Instead, it is marked for removal and will be removed as soon as its current interval is over (it will not run again after being marked for removal).

You might want to add jobs in response to certain user input, and there is a convenient way to do that. The `context` argument of your `Handler` callbacks has the `JobQueue` attached as `context.job_queue` ready to be used. Another feature you can use here is the `context` keyword argument of `Job`. You can pass any object as a `context` parameter when you launch a `Job` and retrieve it at a later stage as long as the `Job` exists. Let's see how it looks in code:

```python
from telegram.ext import CommandHandler
def callback_alarm(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=context.job.context, text='BEEP')

def callback_timer(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Setting a timer for 1 minute!')

    context.job_queue.run_once(callback_alarm, 60, context=update.message.chat_id)

timer_handler = CommandHandler('timer', callback_timer)
u.dispatcher.add_handler(timer_handler)
```

By placing the `chat_id` in the `Job` object, the callback function knows where it should send the message.

All good things must come to an end, so when you stop the Updater, the related job queue will be stopped as well:

```python
u.stop()
```

Of course, you can instead also stop the job queue by itself:

```python
j.stop()
```
