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
        """Сумма произведений цены на количество двух товаров.

        Разрешено складывать только объекты ОДНОГО класса (type()).
        """
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Класс Smartphone — наследник Product"""

    def __init__(self, name: str, description: str, price: float, quantity: float,
                 efficiency: float, model: str, memory: int, color: str) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = float(efficiency)  # производительность
        self.model = model  # модель
        self.memory = int(memory)  # объём встроенной памяти
        self.color = color  # цвет


class LawnGrass(Product):
    """Класс LawnGrass — наследник Product"""

    def __init__(self, name: str, description: str, price: float, quantity: float,
                 country: str, germination_period: str, color: str) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country  # страна-производитель
        self.germination_period = germination_period  # срок прорастания
        self.color = color  # цвет


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
        """Добавляет продукт в приватный список и увеличивает счётчик на 1.

        Разрешены только объекты Product и его наследников (isinstance).
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")
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
    smartphone1 = Smartphone("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5, 95.5,
                         "S23 Ultra", 256, "Серый")
    smartphone2 = Smartphone("Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space")
    smartphone3 = Smartphone("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14, 90.3, "Note 11", 1024, "Синий")

    print(smartphone1.name)
    print(smartphone1.description)
    print(smartphone1.price)
    print(smartphone1.quantity)
    print(smartphone1.efficiency)
    print(smartphone1.model)
    print(smartphone1.memory)
    print(smartphone1.color)

    print(smartphone2.name)
    print(smartphone2.description)
    print(smartphone2.price)
    print(smartphone2.quantity)
    print(smartphone2.efficiency)
    print(smartphone2.model)
    print(smartphone2.memory)
    print(smartphone2.color)

    print(smartphone3.name)
    print(smartphone3.description)
    print(smartphone3.price)
    print(smartphone3.quantity)
    print(smartphone3.efficiency)
    print(smartphone3.model)
    print(smartphone3.memory)
    print(smartphone3.color)

    grass1 = LawnGrass("Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Газонная трава 2", "Выносливая трава", 450.0, 15, "США", "5 дней", "Темно-зеленый")

    print(grass1.name)
    print(grass1.description)
    print(grass1.price)
    print(grass1.quantity)
    print(grass1.country)
    print(grass1.germination_period)
    print(grass1.color)

    print(grass2.name)
    print(grass2.description)
    print(grass2.price)
    print(grass2.quantity)
    print(grass2.country)
    print(grass2.germination_period)
    print(grass2.color)

    smartphone_sum = smartphone1 + smartphone2
    print(smartphone_sum)

    grass_sum = grass1 + grass2
    print(grass_sum)

    try:
        invalid_sum = smartphone1 + grass1
    except TypeError:
        print("Возникла ошибка TypeError при попытке сложения")
    else:
        print("Не возникла ошибка TypeError при попытке сложения")

    category_smartphones = Category("Смартфоны", "Высокотехнологичные смартфоны", [smartphone1, smartphone2])
    category_grass = Category("Газонная трава", "Различные виды газонной травы", [grass1, grass2])

    category_smartphones.add_product(smartphone3)

    print(category_smartphones.products)

    print(Category.product_count)

    try:
        category_smartphones.add_product("Not a product")
    except TypeError:
        print("Возникла ошибка TypeError при добавлении не продукта")
    else:
        print("Не возникла ошибка TypeError при добавлении не продукта")


# python src/approach.py
# black src/approach.py
# flake8 src/approach.py
# mypy src/approach.py
# isort src/approach.py