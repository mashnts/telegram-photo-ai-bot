# Telegram бот для фото и AI

Бот для обработки изображений и общения с AI моделями.

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

## Локальный запуск

```bash
pip install -r requirements.txt
```

Создай `.env` файл с ключами:
```
telegram_bot_token=ваш_токен
openai_api_key=ваш_ключ
replicate_api_token=ваш_токен
```

Запуск:
```bash
python main.py
```
