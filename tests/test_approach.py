import pytest

from src.approach import Category, LawnGrass, Product, Smartphone
from src.approach import BaseProduct, ReprMixin


def test_product_01(entity_names_product_01):
    product1 = entity_names_product_01[0]
    assert product1.name == "Samsung Galaxy S23 Ultra"
    assert product1.description == "256GB, Серый цвет, 200MP камера"
    assert product1.price == 180000.0
    assert product1.quantity == 5

    product2 = entity_names_product_01[1]
    assert product2.name == "Iphone 15"
    assert product2.description == "512GB, Gray space"
    assert product2.price == 210000.0
    assert product2.quantity == 8

    product3 = entity_names_product_01[2]
    assert product3.name == "Xiaomi Redmi Note 11"
    assert product3.description == "1024GB, Синий"
    assert product3.price == 31000.0
    assert product3.quantity == 14

    # создано ровно 3 продукта (счётчик сбрасывается перед каждым тестом)
    assert Product.product_count == 3


def test_category_01(entity_names_category_01):
    category1 = entity_names_category_01

    assert category1.name == "Смартфоны"
    assert (
        category1.description
        == "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )

    # геттер products возвращает СТРОКУ — проверяем построчно
    lines = category1.products.splitlines()
    assert len(lines) == 3
    assert lines[0].startswith("Samsung Galaxy S23 Ultra, 180000.00 руб. Остаток: 5 шт.")
    assert lines[1].startswith("Iphone 15, 210000.00 руб. Остаток: 8 шт.")
    assert lines[2].startswith("Xiaomi Redmi Note 11, 31000.00 руб. Остаток: 14 шт.")

    assert category1.category_count == 1
    # Category.product_count = суммарное число товаров во всех категориях
    assert category1.product_count == 3


def test_category_02(entity_names_product_category_01):
    product4, category2 = entity_names_product_category_01

    assert category2.name == "Телевизоры"
    assert (
        category2.description
        == "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником"
    )

    lines = category2.products.splitlines()
    assert len(lines) == 1
    assert lines[0].startswith('55" QLED 4K, 123000.00 руб. Остаток: 7 шт.')

    assert Category.product_count == 1


def test_new_product_from_dict():
    data = {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5,
    }
    p = Product.new_product(data)

    assert isinstance(p, Product)
    assert p.name == data["name"]
    assert p.description == data["description"]
    assert p.price == data["price"]
    assert p.quantity == data["quantity"]


def test_price_getter_setter_and_validation(capsys):
    p = Product("Test", "Desc", 50.0, 1)
    # геттер возвращает исходную цену
    assert p.price == 50.0

    # отрицательная цена не присваивается, выводится сообщение
    p.price = -5
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert p.price == 50.0

    # нулевая цена тоже не присваивается
    p.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert p.price == 50.0

    # допустимая цена присваивается
    p.price = 20.0
    assert p.price == 20.0


def test_private_price_inaccessible():
    p = Product("Test", "Desc", 10.0, 1)
    with pytest.raises(AttributeError):
        _ = p.__price


def test_category_private_products_and_getter():
    p1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    p2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    cat = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [p1],
    )
    cat.add_product(p2)

    lines = cat.products.splitlines()
    assert len(lines) == 2
    assert lines[0].startswith("Samsung Galaxy S23 Ultra, 180000.00 руб. Остаток: 5 шт.")
    assert lines[1].startswith("Iphone 15, 210000.00 руб. Остаток: 8 шт.")

    # добавление третьего продукта через add_product
    p3 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    cat.add_product(p3)

    lines2 = cat.products.splitlines()
    assert len(lines2) == 3
    assert lines2[2].startswith('55" QLED 4K, 123000.00 руб. Остаток: 7 шт.')

    # add_product прибавляет 1 к счётчику товаров категорий:
    # 1 (при создании) + 1 (p2) + 1 (p3) = 3
    assert Category.product_count == 3
    assert isinstance(cat, Category)


# ---------- Счётчики ----------


def test_product_count_increments(product1, product2, product3):
    assert Product.product_count == 3


def test_category_count_increments(category):
    assert Category.category_count == 1


def test_category_product_count_is_sum_of_products(category):
    # В категорию передано 3 продукта
    assert Category.product_count == 3


# ---------- Цена: геттер и сеттер ----------


def test_price_getter(product1):
    assert product1.price == 180000.0


def test_price_setter_positive(product1):
    product1.price = 150000.5
    assert product1.price == 150000.5


def test_price_setter_rejects_non_positive(product1, capsys):
    product1.price = 0
    assert product1.price == 180000.0
    product1.price = -100
    assert product1.price == 180000.0
    assert "Цена не должна быть нулевая или отрицательная" in capsys.readouterr().out


# ---------- new_product ----------


def test_new_product_from_dict():
    data = {
        "name": "Xiaomi Redmi Note 11",
        "description": "1024GB, Синий",
        "price": 31000.0,
        "quantity": 14,
    }
    product = Product.new_product(data)
    assert isinstance(product, Product)
    assert product.name == "Xiaomi Redmi Note 11"
    assert product.description == "1024GB, Синий"
    assert product.price == 31000.0
    assert product.quantity == 14


# ---------- Геттер products ----------


def test_products_getter_returns_string(category):
    assert isinstance(category.products, str)


def test_products_getter_format(category):
    expected = (
        "Samsung Galaxy S23 Ultra, 180000.00 руб. Остаток: 5 шт.\n"
        "Iphone 15, 210000.00 руб. Остаток: 8 шт.\n"
        "Xiaomi Redmi Note 11, 31000.00 руб. Остаток: 14 шт.\n"
    )
    assert category.products == expected


# ---------- add_product ----------


def test_add_product_increases_count(category, product1):
    category.add_product(product1)
    assert Category.product_count == 4


def test_add_product_appears_in_getter(category, product1):
    category.add_product(product1)
    assert category.products.count("Samsung Galaxy S23 Ultra") == 2


# ---------- __str__ ----------


def test_product_str(product1):
    assert str(product1) == "Samsung Galaxy S23 Ultra, 180000.00 руб. Остаток: 5 шт."


def test_product_str_float_quantity():
    product = Product("Тест", "Описание", 99.9, 5.5)
    assert str(product) == "Тест, 99.90 руб. Остаток: 5.5 шт."


def test_category_str_sums_quantities(category):
    # 5 + 8 + 14 = 27
    assert str(category) == "Смартфоны, количество продуктов: 27 шт."


def test_category_str_float_total():
    p1 = Product("A", "desc", 10.0, 1.5)
    p2 = Product("B", "desc", 20.0, 2.5)
    cat = Category("Категория", "описание", [p1, p2])
    assert str(cat) == "Категория, количество продуктов: 4 шт."


# ---------- __add__ ----------


def test_add_exact_values(product1, product2):
    # 180000 * 5 + 210000 * 8 = 2580000
    assert product1 + product2 == 2580000.0


def test_add_general_formula(product1, product2, product3):
    expected = product1.price * product1.quantity + product2.price * product2.quantity
    assert product1 + product2 == expected
    assert product2 + product3 == product2.price * product2.quantity + product3.price * product3.quantity


def test_add_does_not_mutate(product1, product2):
    before = (product1.price, product1.quantity, product2.price, product2.quantity)
    product1 + product2
    assert (product1.price, product1.quantity, product2.price, product2.quantity) == before


# ---------- _format_quantity ----------


@pytest.mark.parametrize(
    "quantity, expected",
    [
        (5.0, "5"),
        (5, "5"),
        (5.5, "5.5"),
        (0.0, "0"),
        (14.0, "14"),
    ],
)
def test_format_quantity(quantity, expected):
    assert Category._format_quantity(quantity) == expected


class TestProduct:
    """Базовый класс Product: счётчик, цена, new_product, __str__, __add__."""

    def test_product_count_increments(self):
        Product("A", "B", 100, 1)
        Product("C", "D", 200, 2)
        assert Product.product_count == 2

    def test_price_property(self):
        p = Product("A", "B", 100.5, 1)
        assert p.price == 100.5

    def test_price_setter_valid(self):
        p = Product("A", "B", 100, 1)
        p.price = 150
        assert p.price == 150.0

    def test_price_setter_invalid_keeps_old(self, capsys):
        p = Product("A", "B", 100, 1)
        p.price = 0
        assert p.price == 100.0
        out = capsys.readouterr().out
        assert "Цена не должна быть нулевая или отрицательная" in out

    def test_new_product(self):
        data = {"name": "A", "description": "B", "price": 100, "quantity": 3}
        p = Product.new_product(data)
        assert isinstance(p, Product)
        assert (p.name, p.price, p.quantity) == ("A", 100.0, 3.0)

    def test_str(self):
        p = Product("A", "B", 100, 5)
        assert str(p) == "A, 100.00 руб. Остаток: 5 шт."

    def test_add_products(self, product1, product2):
        expected = 180000.0 * 5 + 210000.0 * 8
        assert product1 + product2 == expected

    def test_add_product_with_smartphone_raises(self, product1, smartphone1):
        with pytest.raises(TypeError):
            product1 + smartphone1


class TestSmartphone:
    """Наследник Smartphone: атрибуты, наследование, сложение."""

    def test_attributes(self, smartphone1):
        assert smartphone1.efficiency == 95.5
        assert smartphone1.model == "S23 Ultra"
        assert smartphone1.memory == 256
        assert smartphone1.color == "Серый"

    def test_is_product(self, smartphone1):
        assert isinstance(smartphone1, Product)
        assert smartphone1.name == "Samsung Galaxy S23 Ultra"
        assert smartphone1.price == 180000.0

    def test_str(self, smartphone1):
        assert str(smartphone1) == "Samsung Galaxy S23 Ultra, 180000.00 руб. Остаток: 5 шт."

    def test_add_smartphones(self, smartphone1, smartphone2):
        expected = 180000.0 * 5 + 210000.0 * 8
        assert smartphone1 + smartphone2 == expected

    def test_new_product_returns_smartphone(self):
        data = {"name": "A", "description": "B", "price": 100, "quantity": 1}
        assert isinstance(Smartphone.new_product(data), Smartphone)


class TestLawnGrass:
    """Наследник LawnGrass: атрибуты, наследование, сложение."""

    def test_attributes(self, grass1):
        assert grass1.country == "Россия"
        assert grass1.germination_period == "7 дней"
        assert grass1.color == "Зеленый"

    def test_is_product(self, grass1):
        assert isinstance(grass1, Product)

    def test_add_grasses(self, grass1, grass2):
        expected = 500.0 * 20 + 450.0 * 15
        assert grass1 + grass2 == expected

    def test_add_grass_and_smartphone_raises(self, grass1, smartphone1):
        with pytest.raises(TypeError):
            grass1 + smartphone1


class TestCategory:
    """Категория: счётчики, добавление, геттер products, __str__, форматирование."""

    def test_category_count(self):
        Category("A", "B", [])
        Category("C", "D", [])
        assert Category.category_count == 2

    def test_product_count_on_init(self, product1, product2):
        Category("A", "B", [product1, product2])
        assert Category.product_count == 2

    def test_product_count_includes_subclasses(self, smartphone1, grass1):
        Category("A", "B", [smartphone1, grass1])
        assert Category.product_count == 2

    def test_add_product_increments_counter(self, product1):
        category = Category("A", "B", [])
        category.add_product(product1)
        assert Category.product_count == 1

    def test_add_smartphone_allowed(self, smartphone1):
        category = Category("A", "B", [])
        category.add_product(smartphone1)
        assert Category.product_count == 1
        assert "Samsung Galaxy S23 Ultra" in category.products

    def test_add_not_product_raises(self):
        category = Category("A", "B", [])
        with pytest.raises(TypeError):
            category.add_product("Not a product")

    def test_add_int_raises(self):
        category = Category("A", "B", [])
        with pytest.raises(TypeError):
            category.add_product(42)

    def test_products_getter(self, product1, product2):
        category = Category("Смартфоны", "Тест", [product1, product2])
        expected = (
            "Samsung Galaxy S23 Ultra, 180000.00 руб. Остаток: 5 шт.\n" "Iphone 15, 210000.00 руб. Остаток: 8 шт.\n"
        )
        assert category.products == expected

    def test_str_sum_of_quantities(self, product1, product2, product3):
        category = Category("Смартфоны", "Тест", [product1, product2, product3])
        assert str(category) == "Смартфоны, количество продуктов: 27 шт."

    def test_format_quantity_integer(self):
        assert Category._format_quantity(5.0) == "5"

    def test_format_quantity_float(self):
        assert Category._format_quantity(5.5) == "5.5"


class TestBaseProduct:
    """Абстрактный базовый класс."""

    def test_base_product_cannot_be_instantiated(self):
        """BaseProduct абстрактный — создать экземпляр напрямую нельзя."""
        with pytest.raises(TypeError):
            BaseProduct("Телефон", "Описание", 1000.0, 1)

    def test_product_is_subclass_of_base_product(self):
        assert issubclass(Product, BaseProduct)

    def test_smartphone_and_grass_inherit_base_interface(self):
        assert issubclass(Smartphone, BaseProduct)
        assert issubclass(LawnGrass, BaseProduct)

    def test_smartphone_and_grass_inherit_only_from_product(self):
        """Smartphone и LawnGrass наследуются только от Product."""
        assert Smartphone.__bases__ == (Product,)
        assert LawnGrass.__bases__ == (Product,)


class TestReprMixin:
    """Миксин: печать информации о созданном объекте."""

    def test_mixin_is_in_product_mro(self):
        assert ReprMixin in Product.__mro__

    def test_product_creation_prints_class_and_params(self, capsys):
        Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5)
        out = capsys.readouterr().out
        assert "Создан объект класса Product" in out
        assert "Samsung Galaxy S23 Ultra" in out
        assert "price=180000.0" in out
        assert "quantity=5.0" in out

    def test_smartphone_creation_prints_class_name(self, capsys):
        Smartphone("iPhone 15", "512GB, Gray space", 210000.0, 8, 90.0, "15", 256, "серый")
        out = capsys.readouterr().out
        assert "Создан объект класса Smartphone" in out

    def test_lawn_grass_creation_prints_class_name(self, capsys):
        LawnGrass("Газон", "Трава", 500.0, 10, "Россия", "7 дней", "зелёный")
        out = capsys.readouterr().out
        assert "Создан объект класса LawnGrass" in out

    def test_category_does_not_print(self, capsys):
        """Category не использует миксин — вывода быть не должно."""
        Category("Смартфоны", "Описание", [])
        assert capsys.readouterr().out == ""


# python tests/test_approach.py
# black tests/test_approach.py
# flake8 tests/test_approach.py
# mypy tests/test_approach.py
# isort tests/test_approach.py
# pytest
