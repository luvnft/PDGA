from django.urls import include, path
from django.contrib import admin
from . import views

handler429 = 'history.views.rate_limit_exceeded'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('ping/', views.ping, name='ping'),
]