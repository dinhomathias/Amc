## Introduction
Our examples usually start the bot using `Updater.start_polling`. This method uses the [getUpdates](https://core.telegram.org/bots/api#getupdates) API method to receive new updates for your bot. This is fine for smaller to medium-sized bots and for testing, but if your bot receives a lot of traffic, it might slow down the response times. There might be other reasons for you to switch to a webhook-based method for update retrieval.

**First things first:** You should have a good reason to switch from polling to a webhook. Don't do it simply because it sounds cool. Or do it anyways, I'm not your mother.

## Polling vs. Webhook
The general difference between polling and a webhook is: 

- Polling (via `getUpdates`) periodically connects to Telegram servers to check for new updates
- A Webhook is a URL you transmit to Telegram once. Whenever a new update for your bot arrives, Telegram sends that update to the specified URL.

## Requirements
There's a number of things you need to retrieve updates via webhook.

### A public IP address or domain
Usually this means you have to run your bot on a server, either a dedicated server or a VPS. Read [Where to host Telegram Bots](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Where-to-host-Telegram-Bots) to find a list of options. 

Make sure you can connect to your server from the **public internet**, either by IP or domain name. If `ping` works, you're good to go.

### A SSL certificate
All communications with the Telegram Servers must be encrypted with HTTPS using SSL. When using polling, this is taken care of by the Telegram Servers, but if you want to receive updates via Webhook, you have to take care of it. Telegram will not send you any updates if you don't.

There are two ways to do this: 

1. A verified certificate issued by a trusted certification authority (CA)
2. A self-signed certificate

If you don't already have a verified certificate, use a self-signed one. It's easier and there is no disadvantage to it.

#### Creating a self-signed certificate using openssl
To create a self-signed SSL certificate using `openssl`, run the following command:
```
openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 3650 -out cert.pem
```

The `openssl` utility will ask you a few details. **Make sure you enter the correct FQDN!** If your server has a domain, enter the full domain name here (eg. `sub.example.com`). If your server only has an IP address, enter that instead. If you enter an invalid FQDN (Fully Qualified Domain Name), you won't receive any updates from Telegram but also won't see any errors!

## Choosing a server model
There actually is a third requirement: A HTTP server to listen for webhook connections. At this point, there are several things to consider, depending on your needs. 

### The integrated webhook server
The `python-telegram-bot` library ships a custom HTTP server, based on the CPython `BaseHTTPServer.HTTPServer` implementation, that is tightly integrated in the `telegram.ext` module and can be started using `Updater.start_webhook`. This webserver also takes care of decrypting the HTTPS traffic. It is probably the easiest way to set up a webhook.

However, there is a limitation with this solution. Telegram currently only supports four ports for webhooks: *443, 80, 88* and *8443.* As a result, you can only run a **maximum of four bots** on one domain/IP address. 

If that's not a problem for you (yet), you can use the code below (or similar) to start your bot with a webhook. The `listen` address should either be `'0.0.0.0'` or, if you don't have permission for that, the public IP address of your server. The port can be one of `443`, `80`, `88` or `8443`. For the `url_path`, it is recommended to use your Bot's token, so no one can send fake updates to your bot. `key` and `cert` should contain the path to the files you generated [earlier](#creating-a-self-signed-certificate-using-openssl). The `webhook_url` should be the actual URL of your webhook. Include the `https://` protocol in the beginning, use the domain or IP address you set as the FQDN of your certificate and the correct port and URL path.

```python
updater.start_webhook(listen='0.0.0.0',
                      port=8443,
                      url_path='TOKEN',
                      key='private.key',
                      cert='cert.pem',
                      webhook_url='https://example.com:8443/TOKEN')
```

### Reverse proxy + integrated webhook server
To solve this problem, you can use a reverse proxy like *nginx* or *haproxy*. For this to work, **you need a domain** for your server. 

In this model, each bot is assigned their own *subdomain*. If your server has the domain *example.com*, you could have the subdomains *bot1.example.com*, *bot2.example.com* etc. The reverse proxy performs the *SSL termination* (meaning it decrypts the HTTPS connection), identifies the correct bot and forwards the decrypted traffic to an *integrated webserver* running on an arbitrary port. This port does not have to be one of the four ports mentioned earlier. It also means that the integrated webserver does not have to decrypt the incoming traffic anymore.

Use the code below (or similar) to start the integrated webhook server. The server can be started on the `localhost` or `127.0.0.1` address, the port can be any port you choose. **Note:** In this server model, you have to call `setWebhook` yourself.

```python
updater.start_webhook(listen='127.0.0.1', port=5000, url_path='TOKEN')
updater.bot.setWebhook(url='https://bot1.example.com/TOKEN',
                       certificate=open('cert.pem', 'rb'))
```

Example configuration (reduced to important parts) for `haproxy` with two bots configured. Again, the FQDN of both certificates must match the value in `ssl_fc_sni`:
```
frontend  public-https
    bind        0.0.0.0:443 ssl crt /[...]/cert_bot1.pem crt /[...]/cert_bot2.pem
    option      httpclose

    use_backend bot1 if  { ssl_fc_sni bot1.example.com }
    use_backend bot2 if  { ssl_fc_sni bot2.example.com }

backend bot1
    mode            http
    option          redispatch
    server          bot1.example.com 127.0.0.1:5000 check inter 1000

backend bot2
    mode            http
    option          redispatch
    server          bot2.example.com 127.0.0.1:5001 check inter 1000
```

### Custom solution
You don't necessarily have to use the integrated webserver *at all*. If you choose to go this way, **you should not use the `Updater` class.** The `telegram.ext` module was designed with this option in mind, so you can still use the `Dispatcher` class to profit from the message filtering/sorting it provides. You will have to do some work by hand, though.

A general skeleton code can be found below.

**Setup part, called once:**

```python
from queue import Queue  # in python 2 it should be "from Queue"
from threading import Thread

from telegram import Bot
from telegram.ext import Dispatcher

def setup(token):
    # Create bot, update queue and dispatcher instances
    bot = Bot(token)
    update_queue = Queue()
    
    dispatcher = Dispatcher(bot, update_queue)
    
    ##### Register handlers here #####
    
    
    # Start the thread
    thread = Thread(target=dispatcher.start, name='dispatcher')
    thread.start()
    
    return update_queue
    # you might want to return dispatcher as well, 
    # to stop it at server shutdown, or to register more handlers:
    # return (update_queue, dispatcher)
```

**Called on webhook** with the decoded `Update` object (use `Update.de_json(json.loads(text))` to decode the update):

```python
def webhook(update):
    update_queue.put(update)
```