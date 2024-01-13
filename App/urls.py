from django.contrib import admin
from django.urls import path
from App import views
from App.views import show_html

urlpatterns = [
    path('a', show_html, name='show_html'),
    path('list_programmers/', views.list_programmers, name='list_programmers'),
]
