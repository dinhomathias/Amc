**WIP! v13.1 is not yet out and these remarks weren't double checked yet!**

Since Bot API 5.0, Telegram made the [Bot API server](https://github.com/tdlib/telegram-bot-api) open source allowing you to host your own instance. For details on what benefits hosting your own instance has and how it works, please see the [official docs](Using a Local Bot API Server).

Bot API 5.0 is supported by PTB since v13.1.

## How to Use a local Bot API Server with PTB

* Before moving your bot from the official server to a self hosted, you need to use the [`log_out`](https://core.telegram.org/bots/api#logout) method.
* Before moving from one self hosted instance to another, you need to use the [`delete_webhook`](https://core.telegram.org/bots/api#deletewebhook) and [`close`](https://core.telegram.org/bots/api#close) methods.
* To make PTB aware that you're not using the official server, pass the following to your `Updater` (or `Bot`):
  * `base_url=your-bot-api-server.com/bot`
  * `base_file_url=your-bot-api-server.com/file/bot`
* When running the server with the `--local` flag, `get_file` will give you the local file path as `file_path`. PTB detects that, so that `get_file(…).download()` just opens the local file instead of downloading it.