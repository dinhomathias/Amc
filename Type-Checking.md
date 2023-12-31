# Using Type Checkers with PTB

Since Python 3.6, static type hinting is established in Python and PTB makes use of it (since v13.0). Static type checking helps to avoid and find errors both in PTBs source code and in your bot code. If you want to take advantage of this, you should use a type checker to check your code. As type checking in general is not PTB specific and a big topic, an introduction to type hinting is beyond the scope of this wiki.

### ℹ️ Note

While static type hints *are* of great value and we try our best to make them as precise as possible, they usually don't have any implications on runtime behavior. It therefore may happen that some type hints are not perfect or outright wrong and we may change & fix them between minor versions without announcement. This may lead to your type checker reporting errors after an upgrade, but it won't introduce bugs into your code.

Please also note that type hinting in Python does not cover all edge cases, so there might be situations where PTB just can't do better.

Of course, you are always welcome to report any type hinting errors through the bug tracker.

## Generic classes in PTB

Some of the classes in `telegram.ext` that may be subclassed by users are generic classes, i.e. subclasses of [`typing.Generic`](https://docs.python.org/3/library/typing.html#typing.Generic).
When subclassing them, the type variables should be specified.
These classes currently are `telegram.ext.Handler`, `telegram.ext.BasePersistence` and `telegram.ext.CallbackContext`.
Please have a look at the respective documentation page for more info on the type variables that these classes accept.