## getUpdates: `network_delay`
The `network_delay` keyword of `Bot.getUpdates` was deprecated in favor of `total_timeout`. This is cleaner and portrays more faithfully what's going on: `total_timeout`  is the timeout in seconds for the whole method, so the `timeout` on telegram servers + additional network latency.

## Botan
Botan was moved from `telegram.utils.botan` to `telegram.contrib.botan`