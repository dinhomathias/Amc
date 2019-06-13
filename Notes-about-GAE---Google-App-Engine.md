**NOTE: This page needs more work**

***

Make sure to add this block to `app.yaml` (see [1393](https://github.com/python-telegram-bot/python-telegram-bot/issues/1393)):

```
env_variables:
    GAE_USE_SOCKETS_HTTPLIB : 'true'
```
Note: This environmental variable applies only to applications developed for the Standard Environment and using Python 2.7 (see (https://cloud.google.com/appengine/docs/standard/python/sockets/))