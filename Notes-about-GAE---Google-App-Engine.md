**NOTE: This page needs more work**

***

Make sure to add this block to `app.yaml` (see [1393](https://github.com/python-telegram-bot/python-telegram-bot/issues/1393)):

```
env_variables:
    GAE_USE_SOCKETS_HTTPLIB : 'true'
```