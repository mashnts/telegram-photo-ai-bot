from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import URL, Click
from .utils import get_device_type, get_browser_info, get_os_info, get_client_ip
from .services import get_location_by_ip, generate_qr_code


def index(request):
    # главная страница с формой создания короткой ссылки
    if request.method == 'POST':
        original_url = request.POST.get('url')
        if original_url:
            url_obj = URL.objects.create(
                original_url=original_url,
                created_by=request.user if request.user.is_authenticated else None
            )
            # TODO: сделать генерацию qr кода асинхронной, щас блокирует запрос
            generate_qr_code(url_obj)
            short_url = request.build_absolute_uri(f'/{url_obj.short_code}')

            return render(request, 'shortener/index.html', {
                'short_url': short_url,
                'url_obj': url_obj,
            })

    return render(request, 'shortener/index.html')


def my_links(request):
    # показываем последние 50 созданных ссылок
    # TODO: добавить пагинацию когда ссылок станет больше
    urls = URL.objects.all().order_by('-created_at')[:50]
    return render(request, 'shortener/my_links.html', {'urls': urls})


def redirect_to_url(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)

    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    device_type = get_device_type(user_agent_string)
    browser = get_browser_info(user_agent_string)
    os = get_os_info(user_agent_string)

    ip = get_client_ip(request)
    country, city = get_location_by_ip(ip)

    Click.objects.create(
        url=url,
        device_type=device_type,
        browser=browser,
        os=os,
        country=country,
        city=city,
        referer=request.META.get('HTTP_REFERER', '')
    )

    return redirect(url.original_url)


def analytics(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)
    stats = url.get_click_stats()
    clicks_by_date = url.get_clicks_by_date()

    dates = [item['date'].strftime('%Y-%m-%d') for item in clicks_by_date]
    counts = [item['count'] for item in clicks_by_date]

    context = {
        'url': url,
        'stats': stats,
        'dates': dates,
        'counts': counts,
    }

    return render(request, 'shortener/analytics.html', context)


def analytics_api(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)
    stats = url.get_click_stats()
    clicks_by_date = url.get_clicks_by_date()

    data = {
        'short_code': url.short_code,
        'original_url': url.original_url,
        'created_at': url.created_at.isoformat(),
        'total_clicks': stats['total_clicks'],
        'by_country': list(stats['by_country']),
        'by_city': list(stats['by_city']),
        'by_device': list(stats['by_device']),
        'by_browser': list(stats['by_browser']),
        'by_os': list(stats['by_os']),
        'clicks_by_date': [
            {
                'date': item['date'].strftime('%Y-%m-%d'),
                'count': item['count']
            }
            for item in clicks_by_date
        ],
    }

    return JsonResponse(data)