@echo off
cd /d %~dp0

if not exist .env (
    copy .env.example .env
    echo created .env file.
) else (
    echo file .env already exist.
)

pip install python-dotenv
pip install pyTelegramBotAPI