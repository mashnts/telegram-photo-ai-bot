from django.db import models
from django.contrib.auth.models import User
import string
import random


class URL(models.Model):
    """Модель для хранения оригинального и короткого URL"""
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=15, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='urls')
    click_count = models.PositiveIntegerField(default=0)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_short_code(length=6):
        """генерирует случайный короткий код из букв и цифр"""
        chars = string.ascii_letters + string.digits
        # TODO: это не очень эффективно при большом количестве ссылок
        # надо будет переделать на более умный алгоритм
        while True:
            code = ''.join(random.choice(chars) for _ in range(length))
            if not URL.objects.filter(short_code=code).exists():
                return code

    def get_click_stats(self):
        """собирает статистику по кликам"""
        from django.db.models import Count
        clicks = self.clicks.all()
        # возвращаем словарь со всей статистикой
        return {
            'total_clicks': self.click_count,
            'by_country': clicks.values('country').annotate(count=Count('id')).order_by('-count'),
            'by_city': clicks.values('city').annotate(count=Count('id')).order_by('-count'),
            'by_device': clicks.values('device_type').annotate(count=Count('id')).order_by('-count'),
            'by_browser': clicks.values('browser').annotate(count=Count('id')).order_by('-count'),
            'by_os': clicks.values('os').annotate(count=Count('id')).order_by('-count'),
        }

    def get_clicks_by_date(self):
        from django.db.models.functions import TruncDate
        from django.db.models import Count

        return self.clicks.annotate(
            date=TruncDate('clicked_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date')

class Click(models.Model):
    """сохраняет информацию о каждом клике по короткой ссылке"""
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)
    device_type = models.CharField(max_length=20, blank=True)
    browser = models.CharField(max_length=50, blank=True)
    os = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    referer = models.URLField(max_length=2000, blank=True)

    class Meta:
        ordering = ['-clicked_at']
        # убрал лишние индексы, пока не нужны
        # TODO: добавить индексы когда будет больше данных

    def __str__(self):
        return f"Click on {self.url.short_code} at {self.clicked_at}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # обновляем счетчик кликов
        if is_new:
            self.url.click_count = self.url.clicks.count()
            self.url.save(update_fields=['click_count'])