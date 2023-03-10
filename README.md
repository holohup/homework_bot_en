## Yandex.Practicum Homework Telegram Bot

For those of us who are tired of constantly refreshing the webpage after sending our work for code review to check its status. Here's a bot that checks for updates every 10 minutes and, if the status has changed, sends a notification via Telegram.

The bot takes full advantage of Yandex.Practicum homework API and Telegram Bot API. It is capable of error handling and reporting on its own - there's no need to restart it after it's launched. Every breath is logged, currently to stdout, but this behavior can be easily adjusted to your needs.

**You've got to be a Yandex.Practicum student to get this bot going - the API
requires an OAuth token from Yandex.**

### Technology stack

The bot has been tested to work with Python 3.7 - 3.10. It also uses Python-Telegram-Bot library v. 13.7 and requests 2.26.0

### Installation

1. Copy and paste the following code into a terminal in a directory where your bots live:
```
git clone https://github.com/holohup/homework_bot_en && cd homework_bot_en
```

2. Acquire all the necessary tokens. 
* Find the @BotFather bot in Telegram, follow the instructions to create a new bot using the /newbot command, and follow the instructions provided to get the Telegram token, and save it somewhere. Also, while you're still in Telegram, find @userinfobot, do a /start and find out your Id.
* Go to https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a and copy the token.

Depending on which path you choose to follow, fill either the _.env.sample_, or the _Dockerfile.sample_ file with those credentials and remove the .sample extension. In the end, you should either have a _.env_ or a _Dockerfile_ (or both) filled with the requisites.

3. There're two ways to install and launch the robot:
- Using a virtual environment
```
 python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python homework.py
```

- As a docker container. This Linux image choice in _Dockerfile_ has been tested to run both an x86- and ARMv7-based architecture (Raspberry Pi running _Raspbian GNU/Linux 11 (bullseye)_). It will most likely also run on other SBCs and flavors of Linux, but it hasn't been tested and might require some adjustments in the _Dockerfile_.

```
docker build -t hwbot . && docker run -d hwbot
```

Have fun!
