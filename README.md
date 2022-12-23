Yandex.Practicum Homework Telegram Bot

For those of us who are tired of constantly refreshing the webpage after sending your work for code review to check it's status. Here's a bot that checks for status updates every 10 minutes and, if the status has changed, sends you a notification via Telegram.

The bot takes full advantage of Yandex.Practicum homework API and is capable of error handling and reporting on it's own - there's no need to restart it after it's launched. Every breath is logged, currently to stdout, but this behaviour can be easily changed.

*You'll need to be a Yandex.Practicum student to get this bot going - the API
requires an OAuth token.*

Installation

```
git clone https://github.com/holohup/homework_bot_en && cd homework_bot_en
```
The second step is to acquire all the necessary tokens. 
* Find the @BotFather bot in Telegram, follow the instructions to create a new bot using the /newbot command and follow the instructions provided to get the Telegram token, save it. Also, while you're still in Telegram, find @userinfobot, do a /start and find out your Id.
* Go to https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a and copy the token.

Depending on which path you choose to follow, fill either the .env.sample, or the Dockerfile.sample file with those credencials and remove the .sample extension. In the end, you should have either _.env_ or _Dockerfile_ (or both) filled with the requisites.

There're two ways to install and launch the robot:
1.
```
 python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python homework.py
```

2. As a docker container on a Raspberry Pi running #Raspbian GNU/Linux 11 (bullseye)#.

```
docker build -t hwbot .
```
```
docker run -d hwbot
```

Have fun!