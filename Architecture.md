# Architecture

![PTB Architecture](https://gcdnb.pbrd.co/images/VYfQoTJBY1Mo.png?o=1)

## Required and optional components

> Explain which components are opt-in and which are opt-out.

* `Updater`
* `JobQueue`
* `CallbackDataCache`
* `Defaults`
* `BasePersistence`
* `ContextTypes`

## Customizing Components

> Explain which components can (or even must) be replaced by custom implementations

* `BasePersistence`
* `BaseRequest`
* `Handler`
* `Application` (special case in the builder pattern)