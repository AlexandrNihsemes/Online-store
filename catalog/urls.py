from django.urls import path

from . import views

urlpatterns = [
    # Главная страница — доступна по / и /home/
    path("", views.HomeView.as_view(), name="home"),
    path("home/", views.HomeView.as_view(), name="home"),
    # Страница контактов
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
    # Добавление товара (должно быть выше маршрута с <int:pk>)
    path("products/add/", views.ProductCreateView.as_view(), name="product_add"),
    # Страница товара
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    # Редактирование и удаление товара
    path("products/<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product_edit"),
    path("products/<int:pk>/delete/", views.ProductDeleteView.as_view(), name="product_delete"),
]
