# How is a Proxy Server is Chosen?
PTB will obtain its proxy configuration in the following order (the first to be found will be used):
1. Programmatic.
2. Using `HTTP_PROXY` environment variable.
3. Using `HTTPS_PROXY` environment variable.
4. Using `ALL_PROXY` environment variable.

# Setting a HTTP(S) Proxy Server Programmatically

If you're using the library which comes installed with PTB for making requests, i.e. `httpx`, then this is how you can setup proxies:
```python
from telegram.ext import ApplicationBuilder

# "USERNAME:PASSWORD@" is optional, if you need authentication:
proxy_url = 'http://USERNAME:PASSWORD@PROXY_HOST:PROXY_PORT'  # can also be a https proxy
app = ApplicationBuilder().token("TOKEN").proxy_url(proxy_url).get_updates_proxy_url(proxy_url).build()
```

In the last line, we setup the proxy such that it'll be used both for making requests to the Bot API like  `Bot.send_message` ([`proxy_url()`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.applicationbuilder.html#telegram.ext.ApplicationBuilder.proxy_url)) and for fetching updates from Telegram ([`get_updates_proxy_url`](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.applicationbuilder.html#telegram.ext.ApplicationBuilder.get_updates_proxy_url)). It is not necessary to setup a proxy for both, you can do it for either of them.

# Working Behind a Socks5 Server
This configuration is supported, but requires an optional/extra python package.
To install:
```bash
pip install python-telegram-bot[socks]
```
```python
from telegram.ext import ApplicationBuilder

proxy_url = "socks5://user:pass@host:port"

app = ApplicationBuilder().token("TOKEN").proxy_url(proxy_url).build()
```

If you're more of an advanced user and would like to customize your proxy setup even further, check out the [docs of httpx](https://www.python-httpx.org/advanced/#http-proxying) for more info.