# Concurrency in PTB


### Multithreading

#### How does it work?
The first thing you should know is that the `telegram.ext` submodule uses multithreading for the different tasks it carries out. `Updater`, `Dispatcher` and `JobQueue` each run in their own thread, separate from the main thread. This is mostly hidden from you, but not completely. For example, the `Updater.start_polling` and `start_webhook` methods are non-blocking, meaning that the execution of your script resumes after calling them (that's why you have to call `Updater.idle`).

**Note:** This library uses the [`threading`](https://docs.python.org/3/library/threading.html) module for all concurrency. Because of the [Global Interpreter Lock](https://wiki.python.org/moin/GlobalInterpreterLock) (you don't need to know what that is), **this does not actually make your code run faster**. The real advantage is that I/O operations like network communication (eg. sending a message to a user) or reading/writing on your hard drive can run concurrently. These usually take very long, compared to the rest of your code (I'm talking >95% here), and especially with networking there's a lot of waiting involved. 

Still, when it comes to handling individual requests, no multithreading is used **by default**. All handler callback functions you register in the Dispatcher are executed in the `dispatcher` thread, one after another. So, if one callback function takes some time to execute, all other requests have to wait for it. 

**Example:** You're running the [Echobot](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot2.py) and two users (*User A* and *User B*) send a message to the bot at the same time. Maybe *User A* was a bit quicker, so his request arrives first, in the form of an `Update` object (*Update A*). The Dispatcher checks the Update and decides it should be handled by the handler with the callback function named `echo`. At the same time, the `Update` of *User B* arrives (*Update B*). But the Dispatcher is not finished with *Update A*. It calls the `echo` function with *Update A*, which sends a reply to *User A*. Sending a reply takes some time (see [Server location](#server-location)), and *Update B* remains untouched during that time. Only after the `echo` function finishes for *Update A*, the Dispatcher repeats the same process for *Update B*.

So, how do you get around that? Note that I said **by default**. To solve this kind of problem, the library provides a way to explicitly run a callback function (or any other function) in a separate thread. Before I show you how that looks, let's see how that affects the situation in our example. After you read this article, you marked the `echo` callback function to run in its own thread. Now, when the Dispatcher determined that the `echo` function should handle *Update A*, it creates a new thread with it as the target and *Update A* as an argument and starts the thread. Immediately after starting the thread, it repeats the process for *Update B* without any further delay. Both replies are sent **concurrently**. 

#### How to use it
I don't want to bore you with *words* any further, so let's see some code! Sticking with the Echobot example, this is how you can mark the `echo` function to run in a thread:

```python
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo, run_async=True))
```

Simple and straightforward, right? So, why did I bore you with all that stuff before?

#### Common Pitfalls
Sadly, programming with threads is rarely simple. There are lots of traps to fall into, and I'll try to give you a few hints on how to spot them. However, this wiki article does not replace ~~your psychiatrist~~ a university lecture on concurrency.

##### Shared state
This is probably the biggest cause of issues with threading, and those issues are hard to fix. So instead of showing you how to fix them, I'll show you how to avoid them altogether. More about that later. 

**A fair warning:** In this section, I'll try to give you a simple talk (if that's possible) on a very complex topic. Many have written about it before, and I'm certainly less qualified than most. As usual, I'll use an example to complement the text, and try to stay in the realm of what's important to you. Please bear with me here.

An example that is often used to illustrate this is that of a bank. Let's say you have been hired by a bank to write a Telegram bot to manage bank accounts. The bot has the command `/transaction <amount> <recipient>`, and because many people will be using this command, you think it's a good idea to make this command asynchronous. ~~You~~ Some unpaid intern wrote the following (**BAD AND DANGEROUS**) callback function:

```python
def transaction(update, context):
  bot = context.bot
  chat_id = update.message.chat_id
  source_id, target_id, amount = parse_update(update)

  bot.send_message(chat_id, 'Preparing...')
  bank.log(BEGINNING_TRANSACTION, amount, source_id, target_id)

  source = bank.read_account(source_id)
  target = bank.read_account(target_id)

  source.balance -= amount
  target.balance += amount

  bot.send_message(chat_id, 'Transferring money...')
  bank.log(CALCULATED_TRANSACTION, amount, source_id, target_id)

  bank.write_account(source)
  bank.write_account(target)
  
  bot.send_message(chat_id, 'Done!')
  bank.log(FINISHED_TRANSACTION, amount, source_id, target_id)

dispatcher.add_handler(CommandHandler('transaction', transaction, run_async=True))
```

I skipped some of the implementation details, so here's a short explanation:

- `parse_update` extracts the user id's of the sender (`source_id`) and receiver (`target_id`) from the message
- `bank` is a globally accessible object that exposes the Python API of the banks operations
  - `bank.read_account` reads a bank account from the bank's database into a Python object
  - `bank.write_account` writes a bank account back to the bank's database
  - `bank.log` must be used to keep a log of all changes to make sure no money is lost

Sadly, ~~you~~ that damn intern fell right into the trap. Let's say there are two morally corrupt customers, *Customer A* with *Account A* and *Customer B* with *Account B*, who both make a transaction simultaneously. *Customer A* sends *Transaction AB* of *$10* to *Customer B*. At the same time, *Customer B* sends a *Transaction BA* of *$100* to *Customer A*.

Now the Dispatcher starts two threads, *Thread AB* and *Thread BA*, almost simultaneously. Both threads read the accounts from the database with the **same** balance and calculate a new balance for both of them. In most cases, one of the two transactions will simply overwrite the other. That's not too bad, but will at least be confusing to the customers. But threads are quite unpredictable and can be [suspended and resumed by the operating system](https://en.wikipedia.org/wiki/Scheduling_(computing)) at *any* point in the code, so the following order of execution can occur:

1. *Thread AB* executes `bank.write_account(source)` and updates *Account A* with *-$10*
2. Before updating *Account B*, *Thread AB* is put to sleep by the operating system
3. *Thread BA* is resumed by the operating system
4. *Thread BA* executes `bank.write_account(source)` and updates *Account B* with *-$100*
5. *Thread BA* also executes `bank.write_account(target)` and updates *Account A* with *+$100*
6. When *Thread AB* is resumed again, it executes `bank.write_account(target)` and updates *Account B* with *+$10*

In the end, *Account A* is at *+$100* and *Account B* is at *+$10*. Of course, this won't happen very often. And that's what makes this bug so critical. It will probably be missed by your tests and end up in production, potentially causing a lot of financial damage.

**Note:** This kind of bug is called a [race condition](https://en.wikipedia.org/wiki/Race_condition) and has been the source of many, many security vulnerabilities. It's also one of the reasons why banking software is not written by unpaid interns.

To be fair, you probably don't write software for banks (if you do, you should already know about this), but this kind of bug can occur in any piece of code that shares *state* across threads. While in this case, the shared state is the `bank` object, it can take many forms. A database, a `dict`, a `list` or any other kind of object that is modified by more than one thread. Depending on the situation, race conditions are more or less likely to occur, and the damage they do is bigger or smaller, but as a rule of thumb, they're bad.

There are many ways to fix race conditions in a multithreaded environment, but I won't explain any of them here. Mostly because it probably isn't worth the work; partly because it's cumbersome and I feel lazy. Instead, as promised in the first paragraph, I'll show you how to avoid them completely. That's not always as easy as it is in this case, but we're lucky:

1. Our set of tools is very limited - `Dispatcher.run_async` is the only thread-related tool we're using
2. Our goals are not very ambitious - we only want to speed up our I/O

There are two relatively simple steps you have to follow. First, identify those parts of the code that **must** run sequentially (the opposite of *in parallel* or *asynchronously*). Usually, that is code that fits **at least one** of these criteria:

1. *Modifies* shared state
2. *Reads* shared state and *relies on* it being correct
3. *Modifies* local state (eg. a variable used later in the same function)

Make sure you have a good idea what *shared state* means. Don't hesitate to do a quick Google search on it. 

I went through our bank example line by line and noted which of the criteria it matches, here's the result:

```python
def transaction(update, context):
  bot = context.bot
  chat_id = update.message.chat_id  # 3
  source_id, target_id, amount = parse_update(update)  # 3

  bot.send_message(chat_id, 'Preparing...')  # None
  bank.log(BEGINNING_TRANSACTION, amount, source_id, target_id)  # None

  source = bank.read_account(source_id)  # 2, 3
  target = bank.read_account(target_id)  # 2, 3

  source.balance -= amount  # 3
  target.balance += amount  # 3

  bot.send_message(chat_id, 'Transferring money...')  # None
  bank.log(CALCULATED_TRANSACTION, amount, source_id, target_id)  # None

  bank.write_account(source)  # 1
  bank.write_account(target)  # 1
  
  bot.send_message(chat_id, 'Done!')  # None
  bank.log(FINISHED_TRANSACTION, amount, source_id, target_id)  # None

dispatcher.add_handler(CommandHandler('transaction', transaction, run_async=True))
```

**Note:** One could argue that `bank.log` modifies shared state. However, logging libraries are usually thread-safe and it's unlikely that the log has a critical functional role. It's not being read from in this function, and I assume it's not being read from anywhere else in the code, so maybe consider this an exception to the rule. Also, for the sake of this example, it'd be boring if only `bot.sendMessage` would be safe to run in parallel. However, we will keep this in mind for the next step.

As you can see, there's a pretty obvious pattern here: `bot.sendMessage` and `bank.log` are not matching any criteria we have set for strictly sequential code. That means we can run this code asynchronously without risk. Therefore, the second step is to extract that code to separate functions and run only them asynchronously. Since our async code parts are all very similar, they can be replaced by a single function. We could have done that before, but then this moment would've been less cool. 

**Note:** Not only handler callbacks can be run asynchronously. The `Dispatcher` has a `run_async` function that let's you run custom functions asynchronously. You can and should use this to your advantage.

```python
def log_and_notify(action, amount, source_id, target_id, chat_id, message):
  bank.log(action, amount, source_id, target_id)
  bot.send_message(chat_id, message)

def transaction(update, context):
  chat_id = update.message.chat_id  # 3
  source_id, target_id, amount = parse_update(update)  # 3

  context.dispatcher.run_async(
    log_and_notify,
    BEGINNING_TRANSACTION,
    amount,
    source_id,
    target_id,
    chat_id,
    'Preparing...',
    update=update
  )

  source = bank.read_account(source_id)  # 2, 3
  target = bank.read_account(target_id)  # 2, 3

  source.balance -= amount  # 3
  target.balance += amount  # 3

  context.dispatcher.run_async(
    log_and_notify,
    CALCULATED_TRANSACTION,
    amount,
    source_id,
    target_id,
    chat_id,
    'Transferring money...',
    update=update
  )

  bank.write_account(source)  # 1
  bank.write_account(target)  # 1
  

  context.dispatcher.run_async(
    log_and_notify,
    FINISHED_TRANSACTION,
    amount,
    source_id,
    target_id,
    chat_id,
    'Done!',
    update=update
  )

dispatcher.add_handler(CommandHandler('transaction', transaction, run_async=False))
```

**Note:** You might have noticed that I moved `bank.log` before `bot.send_message`, so the log entries will be in order *most of the time*, assuming the database operations take long enough for the log to complete.

**Note:** It's likely that `bank.read_account` and `bank.write_account` require some I/O operations to interact with the banks database. You see that it's not always possible to write code asynchronously, at least with this simplified method. Read about [Transactions](https://en.wikipedia.org/wiki/Database_transaction) to learn how databases solve this in "real life".

By separating the strictly sequential code from the asynchronous code, we made sure that no race conditions can occur. The `transaction` function won't be executed concurrently anymore, but we still managed to gain some substantial performance boost over completely sequential code, because the logging and user notification is now run in parallel.

At this point, let me say: **Congratulations!** :tada: and thank you for reading :grin: If you got this far without giving up, please consider a CompSci-related major at university, if you have that opportunity. If I left you with a question or two, post a message in our [Telegram Group](https://telegram.me/pythontelegrambotgroup) and mention @jh0ker. If you found this easy to grasp and/or are eager to learn more about all that threading stuff, consider reading the [documentation of the threading module](https://docs.python.org/3/library/threading.html) or learn about [asyncio](https://docs.python.org/3/library/asyncio.html), a modern and arguably better approach to asynchronous I/O that does not use multithreading.

As you may now have learned, writing good, thread-safe code is no exact science. A few last helpful guidelines for threaded code:

- Avoid using shared state whenever possible
- Write self-contained ([pure](https://en.wikipedia.org/wiki/Pure_function)) functions
- When in doubt, make it sequential
- Asynchronous functions return values encapsulated in a [`Promise`](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/telegram/utils/promise.py)

##### Limits
The maximum of concurrent threads is limited. This limit is 4 by default. To increase this limit, you can pass the keyword argument `workers` to the `Updater` initialization:

```python
updater = Updater(TOKEN, workers=32)
```

If an asynchronous function is called from anywhere, including the Dispatcher, and the limit of concurrent threads is reached, the calling thread will block until one of the threads is done and a slot is free. **Note:** In version 4.3 and later, the calling thread will not block. The following is here for historic reasons.

This can lead to a so-called [deadlock](https://en.wikipedia.org/wiki/Deadlock), especially with nested function calls:

```python
def grandchild():
  pass

def child():
  dispatcher.run_async(grandchild)

def parent():
  dispatcher.run_async(child)
  dispatcher.run_async(child)

dispatcher.run_async(parent)
```

If you limited the maximum amount of threads to 2 and call the `parent` function, you start a thread. This thread calls the `child` function and starts another thread, so the amount of concurrent threads is 2. It now tries to call the `child` function a second time, but has to wait until the just started `child` thread ended. The `child` thread tries to call `grandchild`, but it has to wait until the `parent` thread ended. Now both threads are waiting for each other and blocking all other code that tries to run an asynchronous function. The calling thread (usually the Dispatcher) is effectively dead, hence the term *deadlock*.
