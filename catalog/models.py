from django.db import models


class Category(models.Model):
    """Категория товаров."""

    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар интернет-магазина."""

    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(
        upload_to="products/",
        verbose_name="Изображение",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за покупку",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"


class Contact(models.Model):
    """Контактные данные магазина, выводятся на странице контактов."""

    country = models.CharField(max_length=100, verbose_name="Страна")
    inn = models.CharField(max_length=20, verbose_name="ИНН")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(verbose_name="E-mail")

    class Meta:
        verbose_name = "Контактные данные"
        verbose_name_plural = "Контактные данные"

    def __str__(self):
        return f"{self.country}, {self.address}"
