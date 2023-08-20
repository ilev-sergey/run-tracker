# Run tracker

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Ansible](https://img.shields.io/badge/ansible-%231A1918.svg?style=for-the-badge&logo=ansible&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Telegram Bot API](https://img.shields.io/badge/Telegram_Bot_API-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

This is a telegram bot for storing running activities and tracking your progress.

## Example
![](example.gif)

## Usage

- open the bot at [this link](https://t.me/bot_untaken_bot)
- follow the bot instructions

## Deployment

### Local

- Clone the repository
- Run `pip install -r requirements.txt`
- Create `.env` file in the root repo directory with the following string:
  `BOT_TOKEN = <YOUR_TOKEN>`
- Run `python -m bot.py`

### Docker

#### Using Hub image

```
docker pull nidetag/run-tracker
```
```
docker run --name run-tracker -d -e TOKEN=<YOUR_TOKEN> nidetag/run-tracker
```

#### Building image

```
docker build -t run-tracker .
```
```
docker run --name run-tracker -d -e TOKEN=<YOUR_TOKEN> run-tracker
```
