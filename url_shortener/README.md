# URL Shortener

Простой сокращатель ссылок на Django

## Функции

- Сокращение длинных URL
- Генерация QR кодов
- Аналитика переходов (страны, города, устройства, браузеры)
- График переходов по датам

## Установка

```bash
# клонируем репозиторий
git clone <repo-url>
cd url_shortener

# создаем виртуальное окружение
python -m venv venv
source venv/bin/activate  # на windows: venv\Scripts\activate

# ставим зависимости
pip install -r requirements.txt

# создаем .env файл
cp .env.example .env

# накатываем миграции
python manage.py migrate

# запускаем сервер
python manage.py runserver
```

## TODO

- [ ] добавить кеширование для геолокации
- [ ] сделать генерацию QR кода асинхронной
- [ ] добавить пагинацию для списка ссылок
- [ ] оптимизировать генерацию коротких кодов
- [ ] добавить индексы когда будет много данных

## Технологии

- Django 4.2
- SQLite
- Chart.js для графиков
- QRCode для генерации qr кодов
- ipapi.co для геолокации

## Лицензия

MIT
