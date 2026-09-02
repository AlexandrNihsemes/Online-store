from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех товаров.

    Описывает общий для каждого товара контракт: цену с валидацией,
    строковое представление и операцию сложения. Напрямую экземпляр
    создать нельзя — это абстрактный класс, реализацию даёт Product.
    """

    name: str  # название
    description: str  # описание
    quantity: float  # количество в наличии

    @property
    @abstractmethod
    def price(self) -> float:
        """Геттер цены — обязан реализовать наследник."""

    @price.setter
    @abstractmethod
    def price(self, value: float) -> None:
        """Сеттер цены с валидацией — обязан реализовать наследник."""

    @abstractmethod
    def __str__(self) -> str:
        """Строковое представление товара."""

    @abstractmethod
    def __add__(self, other: "BaseProduct") -> float:
        """Суммарная стоимость двух товаров."""


class ReprMixin:
    """Миксин: при создании объекта выводит в консоль,
    от какого класса и с какими параметрами создан объект.

    Встаёт в MRO до BaseProduct (class Product(ReprMixin, BaseProduct)),
    поэтому super().__init__() из Product.__init__ сначала попадает сюда,
    печатает информацию, а потом уходит дальше по цепочке наследования.
    """

    def __init__(self, *args, **kwargs) -> None:
        params = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        if hasattr(self, "price"):
            params["price"] = self.price
        formatted = ", ".join(f"{key}={value!r}" for key, value in params.items())
        print(f"Создан объект класса {self.__class__.__name__} с параметрами: {formatted}")
        super().__init__()


class Product(ReprMixin, BaseProduct):  # BaseProduct и ReprMixin в цепочке наследования
    """Класс Product"""

    product_count = 0  # общее число созданных продуктов

    name: str  # название
    description: str  # описание
    quantity: float  # количество в наличии

    def __init__(self, name: str, description: str, price: float, quantity: float) -> None:

        if float(quantity) == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        Product.product_count += 1
        self.name = name
        self.description = description
        self.__price = float(price)  # приватный атрибут цены
        self.quantity = float(quantity)
        super().__init__()  # запускает ReprMixin (вывод в консоль)

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

    # значения по умолчанию, чтобы new_product() мог создать смартфон из 4 полей
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: float,
        efficiency: float = 0.0,
        model: str = "",
        memory: int = 0,
        color: str = "",
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = float(efficiency)  # производительность
        self.model = model  # модель
        self.memory = int(memory)  # объём встроенной памяти
        self.color = color  # цвет


class LawnGrass(Product):
    """Класс LawnGrass — наследник Product"""

    # значения по умолчанию (для симметрии со Smartphone)
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: float,
        country: str = "",
        germination_period: str = "",
        color: str = "",
    ) -> None:
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

    def middle_price(self) -> float:
        """Средний ценник всех товаров категории (только self.price).

        Если в категории нет товаров, возвращается 0.
        """
        if not self.__products:
            return 0
        return sum(product.price for product in self.__products) / len(self.__products)

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


if __name__ == "__main__":
    try:
        product_invalid = Product("Бракованный товар", "Неверное количество", 1000.0, 0)
    except ValueError as e:
        print(
            "Возникла ошибка ValueError прерывающая работу программы при попытке добавить продукт с нулевым количеством"
        )
    else:
        print("Не возникла ошибка ValueError при попытке добавить продукт с нулевым количеством")

    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category("Смартфоны", "Категория смартфонов", [product1, product2, product3])

    print(category1.middle_price())

    category_empty = Category("Пустая категория", "Категория без продуктов", [])
    print(category_empty.middle_price())


# python src/approach.py
# black src/approach.py
# flake8 src/approach.py
# mypy src/approach.py
# isort src/approach.py
