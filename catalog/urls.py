from django.urls import path

from . import views

urlpatterns = [
    # Главная страница — доступна по / и /home/
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    # Страница контактов
    path("contacts/", views.contacts, name="contacts"),
]
