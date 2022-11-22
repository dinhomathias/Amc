This page contains useful knowledge bits for writing tests for the PTB library. This might also help you out writing tests for your bots **using** PTB, but that is definitely not the goal of this document. If you have questions writing tests for PTB, feel free to ask them in the [dev group](https://t.me/pythontelegrambotdev). If you want to ask about writing tests for your bots, ask those either in [@pythontelegrambotgroup](https://t.me/pythontelegrambotgroup) or [@pythontelegrambottalk](https://t.me/pythontelegrambottalk).

- [How to generate encrypted passport files](#how-to-generate-encrypted-passport-files)

### How to generate encrypted passport files

For Passport encryption, [decrypting data](https://core.telegram.org/passport#decrypting-data) is clearly laid out by Telegram (for obvious reasons) while they only implicitly explain how they decrypt it. As of writing this document, I could not have been bothered figuring out the exact steps they take to encrypt the file, so I did the following:
* Setup a bot with botfather for passport decryption by providing the public key (with /setpublickey) from [PTBs test private file](../blob/master/tests/data/private.key). As of the time of writing that is <details><summary>this Key.</summary>
-----BEGIN PUBLIC KEY-----<br/>
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAstn3GNj9MRAz7Dsk2bY5<br/>
1//yxadHbYdLr6cro6cWw4JqsTHU3CweFcKuRhw/jOpv37GlTHk1VFrBlhchmvao<br/>
l6zdBLPQPXV5tMa3VQi/y03Y7Ax09C0rndAgjq6Xhsrnx/i1T8AUjBjbeqcuoiVf<br/>
0ZJwatGIODFRtf3CuXZifXlRYgyfrJEP8vd9SfkCHWQabSFE6z0m/vF3Yh4AjsRk<br/>
wugwWVWlOLhmTXHCSsnIPEZhdsuK1E85Nye7H1h68c+wYk07h1b01zlObCmJuS/L<br/>
Ct02JKEHNpCw0DAQF/3C+agLD2CFnN1j+m4RgZqqchVd0tsorGZKG7fMDu6vKOEh<br/>
WwIDAQAB<br/>
-----END PUBLIC KEY-----</details>
* Download the JS SDK and use it as described [here](https://core.telegram.org/passport/sdk-javascript). Fill out the stuff in the examples, don't forget the new lines in the public key. Set scope to the type you want to test.
* Once you press on the button, the tgdesktop app should open, and you can select a file to upload. Either the desktop or the the telegram servers compress pictures on upload and PTBs decryption compares hashes as it should, so have that in mind and download the decrypted part if needed.
* Once you done this, get the update, I copy pasted the json part of the PassportData.
* Setup a Bot object instance with the PTB private key and pass it to PassportData.
* Now you can use PassportData.de_json with the bot instance and the json string to generate a PassportData object.
* From there, you can either get the encrypted elements by accessing .credentials or .data[X], or get the decrypted ones with .decrypted_data().