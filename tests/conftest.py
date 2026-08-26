import sys
from pathlib import Path

import pytest

from src.approach import Product, Category, Smartphone, LawnGrass

# Добавляем корень проекта в sys.path, чтобы работал импорт src.approach
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.approach import Category, Product  # noqa: E402


@pytest.fixture(autouse=True)
def reset_class_counters():
    """Сбрасываем счётчики классов перед каждым тестом.

    Product.product_count / Category.category_count / Category.product_count —
    это атрибуты классов: они накапливаются между тестами, и без сброса
    порядок запуска тестов влиял бы на результат.
    """
    Product.product_count = 0
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def entity_names_product_01():
    """Три продукта для проверки атрибутов Product."""
    return [
        Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5),
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14),
    ]


@pytest.fixture
def entity_names_category_01(entity_names_product_01):
    """Категория «Смартфоны» с тремя продуктами."""
    return Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        entity_names_product_01,
    )


@pytest.fixture
def entity_names_product_category_01():
    """Продукт и категория «Телевизоры» с одним продуктом."""
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4],
    )
    return product4, category2


@pytest.fixture(autouse=True)
def reset_counters():
    """Сбрасывает счётчики классов, чтобы тесты не влияли друг на друга."""
    Product.product_count = 0
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def product1():
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)


@pytest.fixture
def product2():
    return Product("Iphone 15", "512GB, Gray space", 210000.0, 8)


@pytest.fixture
def product3():
    return Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)


@pytest.fixture
def category(product1, product2, product3):
    return Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )


@pytest.fixture(autouse=True)
def reset_counters():
    """Обнуляем счётчики перед каждым тестом, чтобы они не 'протекали'."""
    Product.product_count = 0
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def product1():
    return Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)


@pytest.fixture
def product2():
    return Product("Iphone 15", "512GB, Gray space", 210000.0, 8)


@pytest.fixture
def product3():
    return Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)


@pytest.fixture
def smartphone1():
    return Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера",
                      180000.0, 5, 95.5, "S23 Ultra", 256, "Серый")


@pytest.fixture
def smartphone2():
    return Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")


@pytest.fixture
def smartphone3():
    return Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")


@pytest.fixture
def grass1():
    return LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")


@pytest.fixture
def grass2():
    return LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")


# python tests/conftest.py
# black tests/conftest.py
# flake8 tests/conftest.py
# mypy tests/conftest.py
# isort tests/conftest.py