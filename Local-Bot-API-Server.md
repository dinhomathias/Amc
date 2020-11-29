Since Bot API 5.0, Telegram made the [Bot API server](https://github.com/tdlib/telegram-bot-api) open source, allowing you to host your own instance. For details on what benefits hosting your own instance has and how it works, please see the [official docs](https://core.telegram.org/bots/api#using-a-local-bot-api-server).

Bot API 5.0 (and therefore local API server) is supported by PTB since v13.1.

## How to use a local Bot API Server with PTB

* Before you can move your bot from the official server cloud to a self hosted server, you need to call the [`log_out`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html#telegram.Bot.log_out) method.
* Before moving from one self hosted instance to another, you need to use the [`delete_webhook`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html#telegram.Bot.delete_webhook) and [`close`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.bot.html#telegram.Bot.close) methods.
* To make PTB aware that you're not using the official server, pass the following to your `Updater` (or `Bot`):
  * `base_url='your-bot-api-server.com/bot'`
* If you are running a local bot API server without the `--local` flag, also pass:
  * `base_file_url='your-bot-api-server.com/file/bot'`

### Working with files
* When running the server with the `--local` flag, `get_file` will give you the local file path as `file_path`. PTB detects that, so that `get_file(…).download()` just returns the local file string instead of downloading it.
* When running the server with the `--local` flag, you can send files by passing `'file:///absolute/path/to/file'` instead of an URL or a file handler. Skipping the `'file://'` prefix, passing relative paths (without prefix) or even passing `pathlib.Path` objects is supported as well as a convenience feature by PTB.
* When running the server *without* the `--local` flag, the Bot API server does *not* automatically serve the files obtained by `get_file()`. See [telegram-bot-api/#26](https://github.com/tdlib/telegram-bot-api/issues/26). SO be aware that you have to run a web server which serves them, otherwise you will run into 404 errors.