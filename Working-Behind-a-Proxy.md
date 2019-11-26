# How a Proxy Server is Chosen?
PTB will obtain its proxy configuration in the following order (the first to be found will be used):
1. Programmatic.
2. Using `HTTPS_PROXY` environment variable.
3. Using `https_proxy` environment variable.

# Setting a HTTP Proxy Server Programmatically
```python
# Make sure to import required function

TOKEN='YOUR_BOT_TOKEN'
REQUEST_KWARGS={
    # "USERNAME:PASSWORD@" is optional, if you need authentication:
    'proxy_url': 'http://USERNAME:PASSWORD@PROXY_HOST:PROXY_PORT/',
}

updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
```

# Working Behind a Socks5 Server
This is configuration is supported, but requires an optional/extra python package.
To install:
```bash
pip install python-telegram-bot[socks]
```
```python
TOKEN='YOUR_BOT_TOKEN'
REQUEST_KWARGS={
    'proxy_url': 'socks5 OR socks5h://URL_OF_THE_PROXY_SERVER:PROXY_PORT',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'username': 'PROXY_USER',
        'password': 'PROXY_PASS',
    }
}

updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)