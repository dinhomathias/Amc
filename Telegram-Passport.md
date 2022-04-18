As of Bot API 4.0, Telegram added support for something they call Telegram Passport. It allows a bot developer to receive personal information such as ID documents, phone_number, email and more in a secure encrypted way. This page will teach you most of what you need to know to get starting with Telegram Passport as a bot developer.

If you're here because you received a warning from your bot about not having configured a private key, first be sure that you actually need to use Telegram Passport. If no key is configured, updates sent to your bot with passport data is simply ignored.

Please read the following article describing Telegram Passport from a user's perspective before continuing: [Introducing Telegram Passport](https://telegram.org/blog/passport)

### Step 1) Make sure ptb is up to date

Python-telegram-bot added support for Telegram Passport in version 11.0.0, so first make sure that your installation is up to date by upgrading using:

``` console
$ pip install python-telegram-bot --upgrade
```

### Step 2) Generating keys

Telegram Passport requires that you generate encryption keys so that the data is transmitted securely. More info about asymmetric encryption can be found on [Wikipedia](https://en.wikipedia.org/wiki/Public-key_cryptography).

Then make sure you have `openssl` installed by typing the command below in a console:

```console
$ openssl version
OpenSSL 1.0.2o  27 Mar 2018
```

If your output did not match the above (note that a newer or older version is fine) then you'll need to install openssl. A simple google search for `install openssl on [your OperatingSystem]` should show you how.

Now you can generate your private key.

```console
$ openssl genrsa 2048 > private.key
``` 

This will create a file named `private.key` in your current folder.
**Keep this file private at all times!** Anyone who has this file will be able to decrypt telegram passports meant for you.

Next generate your public key.

```console
$ openssl rsa -in private.key -pubout
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0B
[snip]
KwIDAQAB
-----END PUBLIC KEY-----
```

You will need this key for two things. The first is registering it with @BotFather (next step). The other is every time you wanna call the Telegram Passport API from your website.

### Step 3) Registering with @BotFather
Next you wanna paste the public key you just generated, and then paste it into a chat with @BotFather after sending the `/setpublickey` command to him.

At this point you should also add a privacy policy to your bot if you don't already have one. This can be done via the `/setprivacypolicy` command. Note: this command expects a url, so you will need to host the privacy policy somewhere online.

### Step 4) Set up "Log in with Telegram" button
Now you need to set up the button that your users will press to be able to log in with Telegram. Telegram has written SDK (software development kits) to help you quickly get started with this. In this guide we will only use the Javascript SDK, but the instructions should be easy to adapt to an iOS/macOS or Android app.

Detailed instructions about the Telegram Passport Javascript SDK can be found [here](https://core.telegram.org/passport/sdk-javascript). If you are developing a native app you will instead need to use the [iOS/macOS SDK](https://core.telegram.org/passport/sdk-ios-mac) or the [Android SDK](https://core.telegram.org/passport/sdk-android).

To get started, you will need a simple webpage where you have access to the HTML source code or similar. Then you will need to include the Javascript SDK and then call the `Telegram.Passport.createAuthButton` javascript function.
If you just want to quickly get started we have created a [sample html page example](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/passportbot.html) that you can just download, edit using an editor and then open in your preferred browser. (Note that you will need to [download the actual SDK file](https://github.com/TelegramMessenger/TGPassportJsSDK/blob/master/telegram-passport.js) and put it in the same folder as the HTML file)

Next you will need to fill out your bot id (the numeral part before `:` in your bot token), scope (what data you would like to request), your public key (take care with newlines), the payload, and the callback url.

```javascript
Telegram.Passport.createAuthButton('telegram_passport_auth', {
    bot_id:       BOT_ID, // YOUR BOT ID
    scope:        {data: [{type: 'id_document', selfie: true}, 'address_document', 'phone_number', 'email'], v: 1}, // WHAT DATA YOU WANT TO RECEIVE
    public_key:   '-----BEGIN PUBLIC KEY----- ...', // YOUR PUBLIC KEY
    payload:      'thisisatest', // YOUR BOT WILL RECEIVE THIS DATA WITH THE REQUEST
    callback_url: 'https://example.org' // TELEGRAM WILL SEND YOUR USER BACK TO THIS URL
});
```

Note: For security purposes you should generate a random nonce for each user that visits your site, and ALWAYS verify it with your bot when you receive the passport data. If your site has a python backend something like [itsdangerous](https://pythonhosted.org/itsdangerous/) could come in handy - otherwise other HMAC signing methods should be safe too.

Note: For simple testing using `https://example.org` as the callback_url is fine, but on real sites, this should be set to a url where users will be notified that they've been logged in successfully - after your bot has verified the passport data of course.

Note: The documentation for the scope can be found [here](https://core.telegram.org/passport#passportscope). In the example above we are requesting an ID document (like passport, drivers license etc.) that includes a selfie, a document that shows the users' address, and their phone number and email. You can also use [Telegram Passport > Passport example](https://core.telegram.org/passport/example) to figure out the different scope combinations.

### Step 5) Add a MessageHandler that accepts PassportData elements
Now you wanna add a [MessageHandler](https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.messagehandler.html) to your dispatcher so that you are able to receive [Message](https://python-telegram-bot.readthedocs.io/en/latest/telegram.message.html) elements. This is because the [PassportData](https://python-telegram-bot.readthedocs.io/en/latest/telegram.passportdata.html) will be present as an attribute ([passport_data](https://python-telegram-bot.readthedocs.io/en/latest/telegram.message.html#telegram.Message.passport_data)) of [Message](https://python-telegram-bot.readthedocs.io/en/latest/telegram.message.html). If you want to limit a message handler to only receive Telegram Passports (recommended), use the [filters.PASSPORT_DATA ](https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.filters.html#telegram.ext.filters.StatusUpdate) filter.

In our example folder you will find a [passportbot.py](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/passportbot.py) example bot script. This script will simply decrypt and print all Telegram Passport data that it receives. It will also download all [PassportFiles](https://python-telegram-bot.readthedocs.io/en/latest/telegram.passportfile.html) that it finds to the current directory. To get started with it, replace `TOKEN` with your bot token, and put your `private.key` in the same directory as the script.

### Step 6) Test it!
Last step is simply to run the bot, and then open the webpage in your browser and press the blue "Login with Telegram" button. After configuring a password and uploading the proper documents, you should see the data printed in your console.


