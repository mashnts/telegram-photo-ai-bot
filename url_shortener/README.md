# URL Shortener

Сокращатель ссылок с аналитикой на Django.

## Фичи

- Генерация коротких ссылок
- QR коды
- Аналитика: география, устройства, браузеры
- Графики переходов

## Установка

```bash
git clone https://github.com/yourusername/url_shortener.git
cd url_shortener

python -m venv venv
source venv/bin/activate  # windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Для геолокации создайте `.env`:
```
BASE_URL=http://localhost:8000
```

## Стек

Django 4.2, SQLite, Chart.js, QRCode, ipapi.co
