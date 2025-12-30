import requests
import qrcode
from io import BytesIO
from django.core.files import File
from decouple import config


def get_location_by_ip(ip):
    """получаем страну и город по IP адресу
    TODO: добавить кеширование результатов чтобы не долбить api каждый раз
    """
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=2)
        if response.status_code == 200:
            data = response.json()
            return data.get('country_name', ''), data.get('city', '')
    except:
        # если что-то пошло не так - просто пропускаем
        pass
    return '', ''


def generate_qr_code(url_obj, base_url=None):
    """генерирует qr код для короткой ссылки"""
    if not base_url:
        base_url = config('BASE_URL', default='http://localhost:8000')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    short_url = f"{base_url}/{url_obj.short_code}"
    qr.add_data(short_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    filename = f'qr_{url_obj.short_code}.png'
    url_obj.qr_code.save(filename, File(buffer), save=True)
    buffer.close()
