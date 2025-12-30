from django.urls import path
from . import views

app_name = 'shortener'

urlpatterns = [
    path('', views.index, name='index'),
    path('my-links/', views.my_links, name='my_links'),
    path('analytics/<str:short_code>/', views.analytics, name='analytics'),
    path('api/analytics/<str:short_code>/', views.analytics_api, name='analytics_api'),
    path('<str:short_code>/', views.redirect_to_url, name='redirect'),
]