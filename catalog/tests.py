from django.test import TestCase
from django.urls import reverse

from .models import Category, Product


class CatalogViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Тестовая категория")
        self.product = Product.objects.create(
            name="Тестовый товар",
            description="Описание товара",
            category=self.category,
            price="100.00",
        )

    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail(self):
        response = self.client.get(reverse("product_detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_add(self):
        response = self.client.post(
            reverse("product_add"),
            {
                "name": "Новый товар",
                "description": "Описание нового товара",
                "category": self.category.pk,
                "price": "250.00",
            },
        )
        product = Product.objects.get(name="Новый товар")
        self.assertRedirects(response, reverse("product_detail", kwargs={"pk": product.pk}))

    def test_contacts_page(self):
        response = self.client.get(reverse("contacts"))
        self.assertEqual(response.status_code, 200)

    def test_contacts_form_submit(self):
        response = self.client.post(
            reverse("contacts"),
            {"name": "Иван", "phone": "+7 900 000-00-00", "message": "Здравствуйте"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Спасибо, Иван!")
