O API é exposto através do [telegram.Bot](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/telegram/bot.py) class. Os métodos são os equivalentes de snake_case dos métodos descritos no [Telegram Bot API](https://core.telegram.org/bots/api). Os nomes exatos do método camelCase, como nos documentos do Telegram, também estão disponíveis para sua conveniência. Então, por exemplo `telegram.Bot.send_message` é o mesmo que `telegram.Bot.sendMessage`.

Para gerar um token de acesso(Access Token), você tem que conversar [BotFather](https://t.me/botfather) e siga alguns passos simples (descrito [aqui](https://core.telegram.org/bots#6-botfather)).

Para mais detalhes, consulte a documentação oficial do Telegram em [Bots: An introduction for developers](https://core.telegram.org/bots).

#### Olá, Telegram!

Para ter uma ideia da API e como usá-la com `python-telegram-bot`, **por favor abra uma linha de comando do Python** e siga os próximos passos.

Primeiro, crie uma instância do `telegram.Bot`. `'TOKEN'` deve ser substituído pelo token da API recebido de `@BotFather`:

```python
>>> import telegram
>>> bot = telegram.Bot(token='TOKEN')
```

Para verificar se suas credenciais estão corretas, chame por(call) [getMe](https://core.telegram.org/bots/api#getme) método API:

```python
>>> print(bot.get_me())
{"first_name": "Toledo's Palace Bot", "username": "ToledosPalaceBot"}
```

**Nota:** Os bots não podem iniciar conversas com usuários. Um usuário deve adicioná-los a um grupo ou enviar uma mensagem primeiro. As pessoas podem usar ``telegram.me/<bot_username>`` links ou pesquisa de nome de usuário para encontrar seu bot.

#### O que ler a seguir?
Para ficar real e começar a construir seu primeiro bot usando as classes `telegram.ext`, leia[Extensions – Your first Bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-–-Your-first-Bot)

Se você quiser continuar aprendendo sobre a API, leia [Code snippets](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets).