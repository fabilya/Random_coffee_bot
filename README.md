# Random_Coffee_Bot

<img alt="screenshot" height="300" src="logo.jpg" width="300"/>

## Description
The Random_Coffee_Bot project is a telegram bot that every week (on Mondays) offers to meet with one of the people registered in the bot within the company.
The bot sends out a newsletter with the first and last name of a colleague with whom you need to organize a meeting. Participants are selected randomly, so you can have coffee with people you haven’t met yet at work. There is no need to confirm meetings, participation is optional.

The Random_Coffee_Bot bot implements:
- User registration (during registration, the uniqueness of the email domain is checked, i.e. only company employees can register).
- Storing user data in a Postgres database. Functions for working with the database are implemented asynchronously to improve performance.
- use of the Redis library and server to cache data, improve performance and fault tolerance of the bot.
- Each user can pause or resume participation in mailing lists for meetings.
- Automatic weekly newsletters (on Mondays).
- Changing people randomly, excluding repetitions. The algorithm for selecting a coffee partner is designed to eliminate repetition. Repeating partners is possible only if the person has already met everyone, and more than six months have passed since the last meeting.
- Administration is performed in two ways:
  1. Django admin panel (access via web interface at: http:+ ip of your server)
  2. Directly from the telegram bot (allows you to block or unblock a user by his email).

## Technologies
- Python 3.9
- Aiogram 3.4
- Redis 5.0
- Django 4.2
- APScheduler 3.10
- PostgreSQL 13.10
- Requests 2.31

## Launch of the project
Install the Random_Coffee_Bot project on your server.

In the root directory of the project <your_server>/:~random_coffee_bot, create a file with environment variables .env.
To do this, enter the command: ``` sudo touch .env```.
Next, open the .env file using the command ```sudo nano .env``` and fill it with data as follows:

```
# Variables for PostgreSQL
POSTGRES_DB=test_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Variables for Django project:
SECRET_KEY='django-insecure-7f8jl#&fox9p+zm7@e2!8q66&+%+ex94vwe4razd8t5x+g5!qk'
DEBUG=False
HOST_IP='158.160.16.218'

# Variables for telegram bot
BOT_TOKEN=your bot token
REDIS_HOST=redis
REDIS_PORT=6379
ALLOWED_DOMAIN=@groupeseb
```

### Please note that you must obtain BOT_TOKEN yourself in advance when creating and registering a bot chat
### in the telegram service for creating bots https://t.me/BotFather

## Using a telegram bot:
- To get started, go to the Random_Coffee_Bot chat, click the "Menu" button and then the "/start" pop-up button.
- If you have not yet registered, the bot will prompt you to enter your first and last name. After entering your first and last name, enter your corporate email. After successful registration, the bot will respond to you with the message “You are registered”
- Once you register, you automatically become a member of the meeting mailing lists.
- If you do not want to continue participating, click the "Suspend participation" button. If you would like to continue participating, click the “Resume Participation” button.

## Administration in the Django admin panel:
The Django admin panel is available at: http:+ ip of your server.
If you have administrator rights, the following options are available in the admin panel:
- View and manage chat users. Management includes blocking/unblocking the user, assigning administrator rights, activating/deactivating the user, changing mail and changing the user's first and last name, as well as deleting the user.
- View and delete meetings scheduled by the telegram bot.
- View and manage mailings. The administrator can create, edit or delete mailings. When creating or editing a mailing, the text, date and time of the mailing are indicated.

## Administration from a telegram bot:
To administer directly from a telegram bot, you need to enter the command ```/admin```. After this, the bot will offer access to administrative functions through the admin panel website (see above) or enter the user’s email to block/unblock him.
After entering the user's email, the bot will provide you with user data (first and last name, nickname, full name in tg) and the option to block/unblock or cancel your action.

## Project authors:
[Fabiyanskiy Ilya](https://github.com/fabilya)\
[Ten Alexey](https://github.com/aten88)\
[Boyko Maxim](https://github.com/Boikomp)\
[Khlestov Andrey](https://github.com/AndreyKhlestov)\
[Steblev Konstantin](https://github.com/KonstantinSKS)
