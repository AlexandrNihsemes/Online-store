import pytest

from src.approach import Category, Product


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


# python tests/test_approach.py
# black tests/test_approach.py
# flake8 tests/test_approach.py
# mypy tests/test_approach.py
# isort tests/test_approach.py
# pytest