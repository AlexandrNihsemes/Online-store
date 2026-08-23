class Product:
    """Класс Product"""

    product_count = 0  # общее число созданных продуктов

    name: str  # название
    description: str  # описание
    quantity: float  # количество в наличии

    def __init__(self, name: str, description: str, price: float, quantity: float) -> None:
        Product.product_count += 1
        self.name = name
        self.description = description
        self.__price = float(price)  # приватный атрибут цены
        self.quantity = float(quantity)

    @property
    def price(self) -> float:
        """Геттер цены"""
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        """Сеттер цены с валидацией: цена должна быть положительной"""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        self.__price = float(value)

    @classmethod
    def new_product(cls, product_data: dict) -> "Product":
        """Создаёт экземпляр Product на основе словаря с данными"""
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )

    def __str__(self) -> str:
        """Строковое представление: Название, X руб. Остаток: X шт."""
        qty = float(self.quantity)
        qty_str = str(int(qty)) if qty.is_integer() else str(qty)
        return f"{self.name}, {self.price:.2f} руб. Остаток: {qty_str} шт."

    def __add__(self, other: "Product") -> float:
        """Сумма произведений цены на количество двух товаров"""
        return self.price * self.quantity + other.price * other.quantity


class Category:
    """Класс Category"""

    category_count = 0  # общее число созданных категорий
    product_count = 0  # счётчик продуктов

    name: str  # название
    description: str  # описание

    def __init__(self, name: str, description: str, products: list) -> None:
        Category.category_count += 1
        Category.product_count += len(products)
        self.name = name
        self.description = description
        self.__products = list(products)  # приватный список товаров

    def add_product(self, product: "Product") -> None:
        """Добавляет продукт в приватный список и увеличивает счётчик на 1"""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер: строка со всеми продуктами по шаблону"""
        return "".join(
            f"{product.name}, {product.price:.2f} руб. Остаток: {self._format_quantity(product.quantity)} шт.\n"
            for product in self.__products
        )

    @staticmethod
    def _format_quantity(quantity: float) -> str:
        """Форматирует количество: 5.0 -> '5', 5.5 -> '5.5'"""
        value = float(quantity)
        return str(int(value)) if value.is_integer() else str(value)

    def __str__(self) -> str:
        """Строковое представление: Название, количество продуктов: X шт."""
        total = sum(p.quantity for p in self.__products)
        total_str = str(int(total)) if float(total).is_integer() else str(total)
        return f"{self.name}, количество продуктов: {total_str} шт."


if __name__ == '__main__':
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(str(product1))
    print(str(product2))
    print(str(product3))

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3]
    )

    print(str(category1))

    print(category1.products)

    print(product1 + product2)
    print(product1 + product3)
    print(product2 + product3)


# python src/approach.py
# black src/approach.py
# flake8 src/approach.py
# mypy src/approach.py
# isort src/approach.py