from django.contrib import admin
from .models import URL, Click


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'original_url', 'click_count', 'created_by', 'created_at')
    list_filter = ('created_at', 'created_by')
    search_fields = ('short_code', 'original_url')
    readonly_fields = ('short_code', 'created_at', 'click_count', 'qr_code')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Basic Information', {
            'fields': ('original_url', 'short_code', 'created_by')
        }),
        ('Statistics', {
            'fields': ('click_count', 'created_at')
        }),
        ('QR Code', {
            'fields': ('qr_code',)
        }),
    )


@admin.register(Click)
class ClickAdmin(admin.ModelAdmin):
    list_display = ('url', 'clicked_at', 'country', 'city', 'device_type', 'browser', 'os')
    list_filter = ('clicked_at', 'country', 'device_type', 'browser', 'os')
    search_fields = ('url__short_code', 'country', 'city')
    readonly_fields = ('url', 'clicked_at', 'device_type', 'browser', 'os', 'country', 'city', 'referer')
    date_hierarchy = 'clicked_at'

    fieldsets = (
        ('URL', {
            'fields': ('url',)
        }),
        ('Time', {
            'fields': ('clicked_at',)
        }),
        ('Device', {
            'fields': ('device_type', 'browser', 'os')
        }),
        ('Geolocation', {
            'fields': ('country', 'city')
        }),
        ('Additional', {
            'fields': ('referer',)
        }),
    )
