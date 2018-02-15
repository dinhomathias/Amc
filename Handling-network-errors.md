# Background
Network errors can happen at many levels, on the local side, on the remote or somewhere along the way.

It is hard for applications to identify when an error occurs as it is not always something that can be identified in real time but rather when an additional event happens.

Network errors are a problem which each application have to deal with. Each application for its own use case and desired service level. 

# Where things can break?
## Locally (in ptb)
For something to "break" locally we need to close the network socket. This is something that ptb doesn't do voluntarily and basically if you've encountered such a case, it's a bug.

## Remotely on Telegram servers
There is a suspicion that Telegram are closing connections on some conditions. Whether it is true or not we can't really tell. The application should still be able to deal with it.

## Somewhere along the way
* A flaky network connection can cause connections to seem alive although they are useless.
* Datacenters or ISPs which cut (probably inactive) network connections.
  * Azure drops inactive connections after 4 minutes by default (https://azure.microsoft.com/en-us/blog/new-configurable-idle-timeout-for-azure-load-balancer/).

# How to mitigate?

## Analysis
There is no one way to handle networking issues. Each bot has its own usage pattern and unique network behaviour.

Some bots will require to provide answer to user requests within a limited time, while others can take all the time they need. Some bots will be ok with "loosing" a sent message once in a while, while others must ensure that the message was sent within a limited time frame. Some bots sends big files, while others only receive small files. etc. etc.

In addition, the network connection takes an important factor. Hosting your bot in a region with poor Internet (bandwidth / packet lost / disconnections) is the obvious example but it is not the only problem. In case the bot is hosted "far" from the Telegram Bot servers you'll experience greater latency and possibly more packet loss. TCP should be able to handle packet loss, however, there are side effects for that (when will TCP identify the loss of a packet? what will be the window size? etc.).

Hosting the bot on a slow server can also affect performance and may be observed as networking issues.

Once you've understood the usage pattern of your bot (that includes the QoS) you can go into fine tuning the ptb library for your needs.

## Tweaking ptb
### urllib3 tweaks
ptb performs HTTPS requests using `urllib3`. `urllib3` provides control over `connect_timeout` & `read_timeout`. `urllib3` does not separate between what would be considered read & write timeout, so `read_timeout` serves for both. The defaults chosen for each of these parameters is 5 seconds.

The `read_timeout` is overwritten to 20 seconds when using send methods which attach files (`send_audio`, `send_document`, etc.).
When sending big files, calling `Bot.send_*(timeout=BIGGER_VALUE)` might be a good idea.

The `connect_timeout` value controls the timeout for establishing a connection to the Telegram server(s).

Changing the defaults of `read_timeout` & `connet_timeout` is done when initializing the `Updater`. For example:
```python
Updater(..., request_kwargs={'read_timeout': 6, 'connect_timeout': 7})
```

### getUpdates
`getUpdates` is achieved using [Long Polling](https://en.wikipedia.org/wiki/Push_technology#Long_polling) waiting for the Telegram servers with a [(Telegram defined) timeout](https://core.telegram.org/bots/api#getupdates) of X seconds to respond with new `Update`(s). If a network error occurs during that timeout, it will be discovered only after the timeout had passed.

To be specific, when using the raw API (i.e. using `Bot` directly), the value you pass for `timeout` is added to the value of `read_latency` and that is the exact timing when the error will be detected. In that mode, the default value of `timeout` is 0 and the default value of `read_latency` is 2.

If you're using `Updater` then the default value of `timeout` is overridden to 10. That means that the average time to identify network error is 6 seconds. 

Depending on the SLA you'd like to provide, if you suffer from frequent errors during `getUpdates` consider lowering the `timeout` value to catch the errors faster. Please take in mind that too short polling intervals may have undesirable side effects:
* Telegram servers might conceive it as abusive and block your bot.
* Increase the load on your server and network connection.

### Socket options
Depending on your OS you may be able to set socket options to perform low level tweaks.
At the moment, ptb is setting (hardcoded):
* On all OSes:
```
socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1
socket.IPPROTO_TCP, socket.TCP_NODELAY, 1
```

* On Linux only:
```
socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 120
socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 30
socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 8
```

If you can suggest similar options suitable for other OSes (MS-Windows, MacOS) we're waiting for your PR.

Another community contribution we'll be happy for is fine grained control on the socket options.

## Stabilizing your app
When a network error occurs, be prepared to catch the raised exception and handle it according to your policy (do you want to retry? ignore? other?).

## ptb
If you think of another way to improve stability from within ptb, please contact us (the maintainers).