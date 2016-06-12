## Introduction
When your bot becomes popular, you will eventually want to improve response times. After all, Telegram places high priority on fast messaging. At the same time, responses become slower as more people are using your bot at the same time. This happens more quickly for inline bots, as they may receive multiple inline queries during one interaction. 

There are of course many ways to tackle this problem. I'll talk about the two things that, in my experience, get you the biggest "bang for the buck". The first is using threads to *handle requests asynchronously*, the second is *choosing a good server location.*

### Threading

#### How does it work?
The first thing you should know is that the `telegram.ext` submodule uses multi-threading for the different tasks it carries out. `Updater`, `Dispatcher` and `JobQueue` each run in their own thread, separate from the main thread. This is mostly hidden from you, but not completely. For example, the `Updater.start_polling` and `start_webhook` methods are non-blocking, meaning that the execution of your script resumes after calling them (that's why you have to call `Updater.idle` btw).

**Note:** This library uses the `threading` module for all concurrency. Because of the [Global Interpreter Lock](https://wiki.python.org/moin/GlobalInterpreterLock) (you don't need to know what that is), **this does not actually make your code run faster**. The real advantage is that I/O operations like network communication (eg. sending a message to a user) or reading/writing on your hard drive can run in parallel. These usually take very long, compared to the rest of your code (I'm talking >95% here), and especially with networking there's a lot of waiting involved. 

Still, when it comes to handling individual requests, no multi-threading is used **by default**. All handler callback functions you register in the Dispatcher are executed in the `dispatcher` thread, one after another. So, if one callback function takes some time to execute, all other requests have to wait for it. 

**Example:** You're running the [Echobot](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot2.py) and two users (*User A* and *User B*) send a message to the bot at the same time. Maybe *User A* was a bit quicker, so his request arrives first, in the form of an `Update` object (*Update A*). The Dispatcher checks the Update and decides it should be handled by the handler with the callback function named `echo`. At the same time, the `Update` of *User B* arrives (*Update B*). But the Dispatcher is not finished with *Update A*. It calls the `echo` function with *Update A*, which sends a reply to *User A*. Sending a reply takes some time (see [Server location](#server-location)), and *Update B* remains untouched during that time. Only after the `echo` function finishes for *Update A*, the Dispatcher repeats the same process for *Update B*.

So, how do you get around that? Note that I said **by default**. To solve this kind of problem, the library provides a way to explicitly run a callback function (or any other function) in a separate thread. Before I show you how that looks, let's see how that affects the situation in our example. After you read this article, you marked the `echo` callback function to run in its own thread. Now, when the Dispatcher determined that the `echo` function should handle *Update A*, it creates a new thread with it as the target and *Update A* as an argument and starts the thread. Immediately after starting the thread, it repeats the process for *Update B* without any further delay. Both replies are sent **concurrently**. 

#### How to use it
I don't want to bore you with *knowledge* any further, so let's see some code! Sticking with the Echobot example, this is how you can mark the `echo` function to run in a thread:

At the beginning of your script, import `run_async` like this:

```python
from telegram.ext.dispatcher import run_async
```

Then, use it as a decorator for the `echo` function:

```python
@run_async
def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)
```

This seems quite simple and straightforward, right? So, why did I bore you with all that stuff before?

#### Things to look out for
Sadly, programming with threads rarely is simple and straightforward. There's a lot of traps to fall into, and I'll try to give you a few hints on how to spot them. However, this wiki article does not replace ~~the advice of a doctor~~ a university lecture on concurrency.

##### Shared state
This is probably the biggest cause of issues with threading, and those issues are hard to fix. So instead of showing you how to fix them, I'll show you how to avoid them altogether. More about that later. 

**A fair warning:** In this section, I'll try to give you a simple talk (if that's possible) on a very complex topic. Many have written about it before, and I'm certainly less qualified than most. As usual, I'll use an example to complement the text, and try to stay in the realm of what's important to you. Please bear with me here.

An example that is often used to illustrate this is that of a bank. Let's say you have been hired by a bank to write a Telegram bot to manage bank accounts. The bot has the command `/transaction <amount> <recipient>`, and because many people will be using this command, you think it's a good idea to make this command asynchronous. ~~You~~ Some unpaid intern wrote the following (**BAD AND DANGEROUS**) callback function:

```python
@run_async
def transaction(bot, update):
  chat_id = update.message.chat_id
  source_id, target_id, amount = parse_update(update)

  bot.sendMessage(chat_id, 'Preparing...')
  bank.log(BEGINNING_TRANSACTION, amount, source_id, target_id)

  source = bank.read_account(source_id)
  target = bank.read_account(target_id)

  source.balance -= amount
  target.balance += amount

  bot.sendMessage(chat_id, 'Transferring money...')
  bank.log(CALCULATED_TRANSACTION, amount, source_id, target_id)

  bank.write_account(source)
  bank.write_account(target)
  
  bot.sendMessage(chat_id, 'Done!')
  bank.log(FINISHED_TRANSACTION, amount, source_id, target_id)
```

I skipped some of the implementation details, so here's a short explanation:

- `parse_update` extracts the user id's of the sender (`source_id`) and receiver (`target_id`) from the message
- `bank` is a globally accessable object that exposes the Python API of the banks operations
  - `bank.read_account` reads a bank account from the bank's database into a Python object
  - `bank.read_account` writes a bank account back to the bank's database
  - `bank.log` must be used to keep a log of all changes to make sure no money is lost

Sadly, ~~you~~ that damn intern fell right into the trap. Let's say there are two morally corrupt customers, *Customer A* with *Account A* and *Customer B* with *Account B*, who both make a transaction simultaneously. *Customer A* sends *Transaction AB* of *10CU* to *Customer B*. At the same time, *Customer B* sends a *Transaction BA* of *100CU* to *Customer A*. CU simply means **C**urrency **U**nit like Dollar or Euro.

Now the Dispatcher starts two threads, *Thread AB* and *Thread BA*, almost simultaneously. Both threads read the accounts from the database with the **same** balance and calculate a new balance for both of them. In most cases, one of the two transactions will simply overwrite the other. That's not too bad, but will at least be confusing to the customers. But threads are quite unpredictable and can be [suspended and resumed by the operating system](https://en.wikipedia.org/wiki/Scheduling_(computing)) at *any* point in the code, so the following order of execution can occur:

1. *Thread AB* executes `bank.write_account(source)` and updates *Account A* with *-10CU*
2. Before updating *Account B*, *Thread AB* is put to sleep by the operating system
3. *Thread BA* is resumed by the operating system
4. *Thread BA* executes `bank.write_account(source)` and updates *Account B* with *-100CU*
5. *Thread BA* also executes `bank.write_account(target)` and updates *Account A* with *+100CU*
6. When *Thread AB* is resumed again, it executes `bank.write_account(target)` and updates *Account B* with *+10CU*

In the end, *Account A* is at *+100CU* and *Account B* is at *+10CU*. Of course, this won't happen very often. And that's what makes this bug so critical. It will probably be missed by your tests and end up in production, potentially causing a lot of financial damage.

**Note:** This kind of bug is called [race condition](https://en.wikipedia.org/wiki/Race_condition) and has been the source of many, many security vulnerabilities. It's also one of the reasons why banking software is not written by unpaid interns.

To be fair, you probably don't write software for banks (if you do, you should already know about this), but this kind of bug can occur in any piece of code that shares *state* across threads. While in this case, the shared state is the `bank` object, it can take many forms. A database, a `dict`, a `list` or any other kind of object that is modified by more than one thread. Depending on the situation, race conditions are more or less likely to occur, and the damage they do is bigger or smaller, but as a rule of thumb, they're bad.

There are many ways to fix race conditions in a multi-threaded environment, but I won't explain any of them here. Mostly, because it probably isn't worth it for you, partly because it's cumbersome and I feel lazy. Instead, as promised in the first paragraph, I'll show you how to avoid them completely. That's not always as easy as it is in this case, but that's because the set of tools we're working with is very limited (`@run_async` is the only thread-thingy we're using) and our goals are not very ambitious (we only want to speed up our I/O).

First, identify those parts of the code that **must** run sequentially (the opposite of *in parallel*, so not asynchronously). Usually, that is code that fits **at least one** of these criteria:

1. *Modifies* shared state
2. *Reads* shared state and *rely on it* being correct
3. *Modifies* local state (eg. a variable used later in the same function)

I went through our bank example line by line and noted which of the criteria it matches, here's the result:

```python
@run_async
def transaction(bot, update):
  chat_id = update.message.chat_id  # 3
  source_id, target_id, amount = parse_update(update)  # 3

  bot.sendMessage(chat_id, 'Preparing...')  # None
  bank.log(BEGINNING_TRANSACTION, amount, source_id, target_id)  # None

  source = bank.read_account(source_id)  # 2, 3
  target = bank.read_account(target_id)  # 2, 3

  source.balance -= amount  # 3
  target.balance += amount  # 3

  bot.sendMessage(chat_id, 'Transferring money...')  # None
  bank.log(CALCULATED_TRANSACTION, amount, source_id, target_id)  # None

  bank.write_account(source)  # 1
  bank.write_account(target)  # 1
  
  bot.sendMessage(chat_id, 'Done!')  # None
  bank.log(FINISHED_TRANSACTION, amount, source_id, target_id)  # None
```

**Note:** One could argue that `bank.log` modifies shared state. However, logging libraries are usually thread-safe and it's unlikely that the log has a critical functional role. It's not being read from in this function, and I assume it's not being read from anywhere else in the code, so this is an exception to the rule. Also, for the sake of the example, it'd be boring if only `bot.sendMessage` would be OK to run in parallel. However, we will keep this in mind for the next step.

As you can see, there's a pretty obvious pattern here: `bot.sendMessage` and `bank.log` are not matching any criteria we have set for strictly sequential code. That means we can run this code asynchronously without risk. Therefore, the second step is to extract that code to separate functions and mark them with `@run_async`. Since our async code parts are all very similar, they can be replaced by a single function. We could have done that before, but then this moment would've been less cool. 

```python
@run_async
def log_and_notify(action, amount, source_id, target_id, chat_id, message):
  bank.log(action, amount, source_id, target_id)
  bot.sendMessage(chat_id, message)

def transaction(bot, update):
  chat_id = update.message.chat_id  # 3
  source_id, target_id, amount = parse_update(update)  # 3

  log_and_notify(BEGINNING_TRANSACTION, amount, source_id, target_id, chat_id, 'Preparing...')

  source = bank.read_account(source_id)  # 2, 3
  target = bank.read_account(target_id)  # 2, 3

  source.balance -= amount  # 3
  target.balance += amount  # 3

  log_and_notify(CALCULATED_TRANSACTION, amount, source_id, target_id, chat_id, 'Transferring money...')

  bank.write_account(source)  # 1
  bank.write_account(target)  # 1
  
  log_and_notify(FINISHED_TRANSACTION, amount, source_id, target_id, chat_id, 'Done!')
```

**Note:** You might have noticed that I moved `bank.log` before `bot.sendMessage`, so the log entries will be in order *most of the time*, assuming the database operations take long enough for the log to complete.

**Note:** The `run_async` decorator can be placed on any function, not only handler callbacks. You can and should use this to your advantage.

At this point, let me say: **Congratulations!** :tada: and thank you for reading :) If you got this far without giving up, please consider a CompSci-related major at university, if you can. If I left you with a question or two, post a message in our [Telegram Group](https://telegram.me/pythontelegrambotgroup) and mention @jh0ker. If you found this easy to grasp and/or are eager to learn more about all that threading stuff, consider [reading this](https://docs.python.org/3/library/threading.html) or learn about [asyncio](https://docs.python.org/3/library/asyncio.html), the modern and arguably better approach to asynchronous IO that's not using threads. 

As you may have learned, writing good, thread-safe code is no exact science. A few helpful guidelines for threaded code: 

- Avoid using shared state whenever possible
- Write self-contained ([pure](https://en.wikipedia.org/wiki/Pure_function)) functions
- When in doubt, make it sequential
- Asynchronous functions can't return values (at least not in this implementation)

##### Limits
The maximum of concurrent threads is limited. This limit is 4 by default. To increase this limit, you can pass the keyword argument `workers` to the `Updater` initialization, like this:

```python
updater = Updater(TOKEN, workers=32)
```

If an asynchronous function is called from anywhere, including the Dispatcher, and the limit of concurrent threads is reached, the calling thread will block until one of the threads is done and a slot is free. **Note:** In version 5.0 and later, the calling thread will not block.

This can lead to a so-called [deadlock](https://en.wikipedia.org/wiki/Deadlock), especially with nested function calls:

```python
@run_async
def grandchild():
  pass

@run_async
def child():
  grandchild()

@run_async
def parent():
  child()
  child()
```

If you limited the maximum amount of threads to 2 and call the `parent` function, you start a thread. This thread calls the `child` function and starts another thread, so the amount of concurrent threads has reached 2. It now tries to call the `child` function a second time, but has to wait until the just started `child` thread ended. The `child` thread tries to call `grandchild`, but it has to wait until the `parent` thread ended. Now both threads are waiting for each other and blocking all other code that tries to run an asynchronous function. The calling thread (usually the Dispatcher) is effectively dead, hence the term *deadlock*.

### Server location
All that multi-threading will only get you *so far*. Another potential bottleneck is the time your server (the computer that runs your bot script) needs to contact the Telegram server. 

As of *June 2016*, there is only one server location for the Bot API, which is in the Netherlands. You can test your connection by running `ping api.telegram.org` on the command line of your server. A good connection should have a stable ping of 50ms or less. A server in Central Europe (France, Germany) can easily archive under 15ms, a server in the Netherlands reportedly archived 2ms ping. Servers in the US, Southeast Asia or China are not recommended to host Telegram bots.

**Note:** When choosing a server for the sole purpose of hosting a Telegram bot, this is the only relevant timing. Even if you are the only user of the bot, there is no advantage in choosing a server close to *you.* 

If you need some suggestions on where to host your bot, read [Where to host Telegram Bots](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Where-to-host-Telegram-Bots).