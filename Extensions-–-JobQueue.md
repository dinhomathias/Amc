## Introduction
The extension class `telegram.ext.JobQueue` allows you to perform tasks with a delay or even periodically. For example to send regular updates to your subscribers.

## Note
The `JobQueue` will see some big improvements with the release of v5.0, which requires changes that are not backwards compatible.

## Usage
The `Updater` will create a job queue for you:

```python
>>> from telegram.ext import Updater
>>> u = Updater('TOKEN')
>>> j = u.job_queue
```

The job queue uses functions for tasks, so we define one and add it to the queue. Usually, when the first job is added to the queue, it wil start automatically. We can prevent this by setting ``prevent_autostart=True``:

```python
>>> def job1(bot):
...     bot.sendMessage(chat_id='@examplechannel', text='One message every minute')
>>> j.put(job1, 60, next_t=0, prevent_autostart=True)
```

You can also have a job that will be executed only once, with a delay:

```python
>>> def job2(bot):
...     bot.sendMessage(chat_id='@examplechannel', text='A single message with 30s delay')
>>> j.put(job2, 30, repeat=False)
```

Now, because we didn't prevent the auto start this time, the queue will start ticking. It runs in a seperate thread, so it is non-blocking. When we stop the Updater, the related queue will be stopped as well:

```python
>>> u.stop()
```

We can also stop the job queue by itself:

```python
>>> j.stop()
```