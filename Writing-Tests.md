In case you want to practice [test-driven development](https://en.wikipedia.org/wiki/Test-driven_development), or ensure your bot still works after consecutive changes ([regression bugs](https://en.wikipedia.org/wiki/Software_regression) are rather common for chatbots), you should write test cases.

## Unit Tests
Unit tests are performed on a logically encapsulated component of the system. The definition of unit tests in contrast to integration tests is that they have no external dependencies.
@Eldinnie has written an initial POC of a unit test framework for python-telegram-bot, but as the library grew it was not maintained. Perhaps you might be able to help us out here and help in completing the project ;)
https://github.com/Eldinnie/ptbtest

### Mocking
_Placeholder_

## Integration Tests
In contrast to unit tests, integration tests may test the system in its eventual environment together with service integrations, such as the Bot API.

In order to test your bot the same way your users will, you can make use of a [userbot](http://telegra.ph/How-a-Userbot-superacharges-your-Telegram-Bot-07-09) library that will send messages to your bot and evaluate whether it responds in the way it should. 
The [TgIntegration library](https://github.com/JosXa/tgintegration/) should cover everything you need.