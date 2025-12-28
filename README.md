# English to Persian Translation Bot

A simple Telegram bot that translates English text into **informal, natural Persian** using **Azure OpenAI GPT-4.1**.

---

## Features

- English → informal Persian translation  
- No emojis, symbols, or English in output  
- Telegram commands: `/start`, `/help`, `/about`  
- Max message length: 4000 characters  

---

## Tech Stack

- Python 3.10+
- Telegram Bot API
- Azure OpenAI (GPT-4.1)
- python-telegram-bot
- python-dotenv

---

## Installation

```bash
pip install python-telegram-bot python-dotenv openai

Set the .env like this:

AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_API_VERSION=2025-04-01-preview
TELEGRAM_TR_BOT_TOKEN=your_telegram_bot_key_here
