# Telegram бот для фото и AI

## Установка

```bash
pip install -r requirements.txt
```

Создайте `.env` файл с ключами:
```
telegram_bot_token=ваш_токен
openai_api_key=ваш_ключ
replicate_api_token=ваш_токен
```

## Запуск

```bash
python main.py
```

## Возможности

- Чат с AI (deepseek)
- Анализ фото через GPT-4 Vision
- Распознавание текста (OCR)
- Распознавание лиц
- Редактирование: изменение размера, ретушь, удаление фона
- Конвертация форматов (PNG/JPEG/WEBP)
- Сжатие изображений

## Команды

- `/start` - меню
- `/conversation` - чат с AI
- `/options` - работа с фото
- `/help` - помощь
- `/stop` - завершить

## Деплой на Render

1. Запушь проект на GitHub
2. Зайди на [render.com](https://render.com) и залогинься через GitHub
3. Создай новый Web Service, выбери свой репо
4. Настройки:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
5. Добавь переменные окружения (Environment):
   - `telegram_bot_token`
   - `openai_api_key`
   - `replicate_api_token`
6. Деплой - бот будет работать 24/7 (засыпает после 15 мин бездействия на бесплатном плане)
