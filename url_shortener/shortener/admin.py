from django.contrib import admin
from .models import URL, Click


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'original_url', 'click_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('short_code', 'original_url')
    readonly_fields = ('short_code', 'created_at', 'click_count')


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ('url', 'clicked_at', 'country', 'device_type', 'browser')
    list_filter = ('device_type', 'browser')
    search_fields = ('url__short_code',)
    readonly_fields = ('url', 'clicked_at')
