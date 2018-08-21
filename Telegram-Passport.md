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

If your output did not match the above (note that a newer or older version is fine) then you'll need to install openssl. A simple google search for `install openssl on [your OperatingSystem]` should should you how.

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

### Step 4) moar stuff...
