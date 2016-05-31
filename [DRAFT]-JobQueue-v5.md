---

### Note: This page is a draft for the not-yet-released v5.0 of this library. See [#307](https://github.com/python-telegram-bot/python-telegram-bot/pull/307)


---


The `JobQueue` allows you to perform tasks with a delay or even periodically. The `Updater` will create one for you:

```python
>>> from telegram.ext import Updater
>>> u = Updater('TOKEN')
>>> j = u.job_queue
```

The job queue uses the `Job` class for tasks. We define a callback function, instantiate a `Job` and add it to the queue.

Usually, when the first job is added to the queue, it will start automatically. We can prevent this by setting `prevent_autostart=True`:

```python
>>> from telegram.ext import Job
>>> def callback_minute(bot, job):
...     bot.sendMessage(chat_id='@examplechannel', text='One message every minute')
...
>>> job_minute = Job(callback_minute, 60.0, next_t=0.0)
>>> j.put(job_minute, prevent_autostart=True)
```

You can also have a job that will be executed only once:

```python
>>> def callback_30(bot, job):
...     bot.sendMessage(chat_id='@examplechannel', text='A single message with 30s delay')
...
>>> j.put(Job(callback_30, 30.0, repeat=False))
```

Now, because we didn't prevent the auto start this time, the queue will start working. It runs in a separate thread, so it is non-blocking.

Jobs can be temporarily disabled or completely removed from the `JobQueue`:

```python
>>> job_minute.enabled = False  # Temporarily disable this job
>>> job_minute.schedule_removal()  # Remove this job completely
```

**Note:** `schedule_removal` does not immediately remove the job from the queue. Instead, it is marked for removal and will be removed as soon as its current interval is over (it will not run again after being marked for removal).

A job can also change its own behavior, as it is passed to the callback function as the second argument:

```python
>>> def callback_increasing(bot, job):
...     bot.sendMessage(chat_id='@examplechannel',
...                     text='Sending messages with increasing delay up to 10s, then stops.')
...     job.interval += 1.0
...     if job.interval > 10.0:
...         job.schedule_removal()
...
>>> j.put(Job(callback_increasing, 1.0))
```

When we stop the Updater, the related queue will be stopped as well:

```python
>>> u.stop()
```

We can also stop the job queue by itself:

```python
>>> j.stop()
```
