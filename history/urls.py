from django.urls import include, path
from django.contrib import admin
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('ping/', views.ping, name='ping'),
]

urlpatterns += staticfiles_urlpatterns()