# Telegram AI Photo Bot

Telegram bot for image processing and AI conversation. Integrates OpenAI GPT-4 Vision and Deepseek AI.

## Features

**AI Functions:**
- AI chat (Deepseek)
- Image analysis (GPT-4 Vision)
- Text recognition (OCR)
- Face detection

**Image Processing:**
- Resize and crop
- Photo enhancement
- Background removal
- Format conversion (PNG/JPEG/WEBP)
- Image compression

## Tech Stack

- Python 3.12
- aiogram
- OpenAI API
- Replicate API
- Deployed on Render.com

## Installation

```bash
pip install -r requirements.txt
```

Create `.env` file:
```env
telegram_bot_token=your_token
openai_api_key=your_key
replicate_api_token=your_token
```

Run:
```bash
python main.py
```

## Commands

- `/start` - Main menu
- `/conversation` - AI chat
- `/options` - Photo tools
- `/help` - Help
- `/stop` - Stop session

## Deployment

Configured for Render.com deployment with Procfile and environment variables.
