from django.urls import path

from . import views

urlpatterns = [
    # Главная страница — доступна по / и /home/
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    # Страница контактов
    path("contacts/", views.contacts, name="contacts"),
    # Добавление товара (должно быть выше маршрута с <int:pk>)
    path("products/add/", views.product_add, name="product_add"),
    # Страница товара
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
]
