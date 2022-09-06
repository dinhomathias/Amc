# Why AWS Lambda

With Heroku removing free tiers it's natural to seek free alternatives. AWS has a free tier with [generous](https://aws.amazon.com/free/) limits. Serverless setup with Lambdas is free for a year and cheap afterward. Resources are only allocated when your bot is triggered, so we need to setup a webhook. There are plenty of articles on how to do that, basically, run `curl -GET https://api.telegram.org/bot{BOT_TOKEN}}/setWebhook?url={GATEWAY_URL | FUNCTION_URL}`

## Limitations

However, AWS Lamda currently doesn't support async invocations for Python, and with PTB v20.x we should work around that. To make it work, feel free to use the following example:

```python
import asyncio
from telegram.ext import Application

application = Application.builder().token(TELEGRAM_API_KEY).build()


def lambda_handler(event, context):
    return asyncio.get_event_loop().run_until_complete(main(event, context))

async def main(event, context):
    application.add_handler(...)
    # Add conversation, command and any other handlers
    
    try:
        logging.info('Trying process update')
    
        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(event["body"]), application.bot)
        )
    
        return {
            "statusCode": 200,
            "result": "Success"
        }

    except Exception as exc:
        return {
            "statusCode": 500,
            "result": "Failure"
        }
```

Lambda setting for **Code** / **Runtime Settings** / **Handler** should point to `{main_file}.lambda_handler`, e.g. `bot.lambda_handler`

This `asyncio` pattern is far from ideal as described [here](https://stackoverflow.com/questions/60455830/can-you-have-an-async-handler-in-lambda-python-3-6), but it works as expected.