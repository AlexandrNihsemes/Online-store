import shutil
import tempfile
from io import BytesIO
from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image as PILImage

from .constants import FORBIDDEN_WORDS
from .forms import ProductForm
from .models import Category, Product


def make_image(name: str = "product.png", image_format: str = "PNG") -> SimpleUploadedFile:
    """Создаёт настоящее изображение, которое пройдёт проверку Pillow."""

    buffer = BytesIO()
    PILImage.new("RGB", (20, 20), color=(40, 120, 200)).save(buffer, format=image_format)
    content_type = "image/png" if image_format == "PNG" else "image/jpeg"
    return SimpleUploadedFile(name, buffer.getvalue(), content_type=content_type)


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

    def test_product_update(self):
        response = self.client.get(reverse("product_edit", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse("product_edit", kwargs={"pk": self.product.pk}),
            {
                "name": "Обновлённый товар",
                "description": "Новое описание",
                "category": self.category.pk,
                "price": "999.99",
            },
        )
        self.assertRedirects(response, reverse("product_detail", kwargs={"pk": self.product.pk}))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Обновлённый товар")
        self.assertEqual(self.product.description, "Новое описание")
        self.assertEqual(str(self.product.price), "999.99")

    def test_product_delete(self):
        response = self.client.get(reverse("product_delete", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse("product_delete", kwargs={"pk": self.product.pk}))
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

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


class ProductFormValidationTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Категория")
        self.valid_data = {
            "name": "Полезный плагин",
            "description": "Помогает автоматизировать рутину",
            "category": self.category.pk,
            "price": "1500.00",
        }

    def test_all_forbidden_words_are_rejected_in_name(self):
        for word in FORBIDDEN_WORDS:
            form = ProductForm(data={**self.valid_data, "name": f"Товар {word.upper()}"})
            self.assertFalse(form.is_valid(), msg=f"слово {word} должно быть запрещено")
            self.assertIn("name", form.errors)

    def test_all_forbidden_words_are_rejected_in_description(self):
        for word in FORBIDDEN_WORDS:
            form = ProductForm(data={**self.valid_data, "description": f"Купите {word.capitalize()} сейчас"})
            self.assertFalse(form.is_valid(), msg=f"слово {word} должно быть запрещено")
            self.assertIn("description", form.errors)

    def test_forbidden_word_error_mentions_word_and_field(self):
        form = ProductForm(data={**self.valid_data, "name": "Казино удачи"})
        self.assertFalse(form.is_valid())
        error = " ".join(form.errors["name"])
        self.assertIn("казино", error.lower())
        self.assertIn("Наименование", error)

    def test_valid_form_passes(self):
        form = ProductForm(data=self.valid_data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_negative_price_is_rejected(self):
        form = ProductForm(data={**self.valid_data, "price": "-100.00"})
        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)
        self.assertIn("отрицательной", " ".join(form.errors["price"]))

    def test_zero_price_is_allowed(self):
        form = ProductForm(data={**self.valid_data, "price": "0.00"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_fields_have_bootstrap_styles(self):
        form = ProductForm()
        self.assertEqual(form.fields["name"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["description"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["price"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["image"].widget.attrs["class"], "form-control")
        self.assertEqual(form.fields["category"].widget.attrs["class"], "form-select")


class ProductImageValidationTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Категория")
        self.media_root = tempfile.mkdtemp()
        self.override = override_settings(MEDIA_ROOT=self.media_root)
        self.override.enable()
        self.data = {
            "name": "Товар с картинкой",
            "description": "Описание товара",
            "category": self.category.pk,
            "price": "500.00",
        }

    def tearDown(self):
        self.override.disable()
        shutil.rmtree(self.media_root, ignore_errors=True)

    def test_png_and_jpeg_are_accepted(self):
        for name, image_format in (("product.png", "PNG"), ("product.jpg", "JPEG")):
            form = ProductForm(data=self.data, files={"image": make_image(name, image_format)})
            self.assertTrue(form.is_valid(), form.errors)

    def test_wrong_format_is_rejected(self):
        form = ProductForm(data=self.data, files={"image": make_image("product.gif", "GIF")})
        self.assertFalse(form.is_valid())
        self.assertIn("JPEG", " ".join(form.errors["image"]))

    def test_too_large_image_is_rejected(self):
        with patch("catalog.forms.MAX_IMAGE_SIZE", 1):
            form = ProductForm(data=self.data, files={"image": make_image()})
            self.assertFalse(form.is_valid())
        self.assertIn("5 МБ", " ".join(form.errors["image"]))

    def test_product_is_saved_with_image(self):
        response = self.client.post(
            reverse("product_add"),
            {**self.data, "image": make_image()},
        )
        product = Product.objects.get(name=self.data["name"])
        self.assertRedirects(response, reverse("product_detail", kwargs={"pk": product.pk}))
        self.assertTrue(product.image.name.endswith(".png"))


class ProductForbiddenWordsViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Категория")
        self.data = {
            "name": "Отличный товар",
            "description": "Описание товара",
            "category": self.category.pk,
            "price": "100.00",
        }

    def test_add_view_shows_error_for_forbidden_word(self):
        response = self.client.post(reverse("product_add"), {**self.data, "name": "Дешевый радар"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "запрещённые слова")
        self.assertFalse(Product.objects.filter(name="Дешевый радар").exists())
