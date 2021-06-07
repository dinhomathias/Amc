# Using Type Checkers with PTB

Since Python 3.6, static type hinting is established in Python and PTB makes use of it (since v13.0). Static type checking helps to avoid and find errors both in PTBs source code and in your bot code. If you want to take advantage of this, you should use a type checker to check your code. As type checking in general is not PTB specific and a big topic, we can't explain everything about it in this wiki. There are however some things that are specific to PTBs type checking and that advanced users might want to keep in mind. More precisely, some classes in `telegram.ext` are `Generics`. Below we detail, how to specify the corresponding types to get proper type checking.

### ℹ️ Note

While static type hints *are* of great value and we try our best to make them as precise as possible, they usually don't have any implications on runtime behavior. It therefore may happen that some type hints are not perfect or outright wrong and we may change & fix them between minor versions without announcement. This may lead to your type checker reporting errors after an upgrade, but it won't introduce bugs into your code.

Of course, you are always welcome to report any type hinting erros through the bug tracker.

## Custom Handlers

```python
class MyHandler(Handler[UpdateClass, CallbackContextClass]):
    ...
```

Here `UpdateClass` should the type of the updates that this handler will handle. In most cases, this will just be `telegram.Update`. However, the handler setup is designed to be able to also handle other objects (e.g., to integrate 3rd party updates into your bot), so this could also be `GitHubUpdateClass` or some other thing.

`CallbackContextClass` is tha type of the `context` argument. In most cases, this will just be `CallbackContext`, but in case you're using a custom type for the `context` argument (see also below), you should pass that instead.

## Custom `CallbackContext` classes

```python
class CustomContext(CallbackContext[UserDataClass, ChatDataClass, BotDataClass]):
    ...
```
The default type for all three is `dict`, which you can use if you don't specify `user/chat/bot_data` for your `ContextTypes` instance.

## Custom persistence classes

```python
class CustomPersistence(BasePersistence[UserDataClass, ChatDataClass, BotDataClass]):
   ...
```
Pretty much the same as for `CallbackContext`


## Custom `Updater`/`Dispatcher`

Depending on whether you use a custom `CallbackContext` class or not, you have two options here:

```python
class CustomUpdaterOrDispatcher(Updater/Dispatcher[CallbackContext[UserDataClass, ChatDataClass, BotDataClass], UserDataClass, ChatDataClass, BotDataClass]):
    ...
```
or
```python
class CustomUpdaterOrDispatcher(Updater/Dispatcher[CustomContext, UserDataClass, ChatDataClass, BotDataClass]):
    ...
```