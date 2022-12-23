## Yandex.Practicum Homework Telegram Bot

For those of us who are tired of constantly refreshing the webpage after sending our work for code review to check it's status. Here's a bot that checks for updates every 10 minutes and, if the status has changed, sends a notification via Telegram.

The bot takes full advantage of Yandex.Practicum homework API and Telegram Bot API  with the help of python-telegram-bot library, is lightweight and effective. It is capable of error handling and reporting on it's own - there's no need to restart it after it's launched. Every breath is logged, currently to stdout, but this behaviour can be easily adjusted to your needs.

**You've got to be a Yandex.Practicum student to get this bot going - the API
requires an OAuth token from Yandex.**

### Requirements

The bot has been tested to work with Python 3.7 - 3.10.

### Installation

1. Copy and paste the following code into a terminal in a directory where your bots live:
```
git clone https://github.com/holohup/homework_bot_en && cd homework_bot_en
```

2. Acquire all the necessary tokens. 
* Find the @BotFather bot in Telegram, follow the instructions to create a new bot using the /newbot command and follow the instructions provided to get the Telegram token, save it. Also, while you're still in Telegram, find @userinfobot, do a /start and find out your Id.
* Go to https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a and copy the token.

Depending on which path you choose to follow, fill either the _.env.sample_, or the _Dockerfile.sample_ file with those credencials and remove the .sample extension. In the end, you should either have an _.env_ or a _Dockerfile_ (or both) filled with the requisites.

3. There're two ways to install and launch the robot:
- Using virtual environment
```
 python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python homework.py
```

- As a docker container on a Raspberry Pi running _Raspbian GNU/Linux 11 (bullseye)_. It will probably run on other SBC's and flavors of Linux, but it hasn't been tested and might need some adjustments in the _Dockerfile_.

```
docker build -t hwbot . && docker run -d hwbot
```

Have fun!