from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = (
        "Загружает тестовые категории и продукты из фикстур, "
        "предварительно удаляя все существующие данные."
    )

    def handle(self, *args, **options):
        self.stdout.write("Удаляем существующие продукты и категории…")
        products_deleted, _ = Product.objects.all().delete()
        categories_deleted, _ = Category.objects.all().delete()
        self.stdout.write(f"Удалено: продуктов — {products_deleted}, категорий — {categories_deleted}")

        self.stdout.write("Загружаем фикстуры categories.json и products.json…")
        call_command("loaddata", "categories.json", verbosity=0)
        call_command("loaddata", "products.json", verbosity=0)

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово: категорий — {Category.objects.count()}, "
                f"продуктов — {Product.objects.count()}"
            )
        )
        for product in Product.objects.select_related("category"):
            self.stdout.write(f"  • {product.name} — {product.price} руб. ({product.category.name})")
