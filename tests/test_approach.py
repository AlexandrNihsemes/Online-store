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


# python tests/test_approach.py
# black tests/test_approach.py
# flake8 tests/test_approach.py
# mypy tests/test_approach.py
# isort tests/test_approach.py
