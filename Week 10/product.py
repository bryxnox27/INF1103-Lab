"""Abstract base class shared by all inventory product types."""

from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    """Common product information and behavior."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
    ) -> None:
        self.__product_id: str = str(product_id).strip()
        self.__name: str = str(name).strip()
        self.__price: float = float(price)
        self.__stock: int = int(stock)
        self.__supplier: Supplier = supplier

        if not self.__product_id:
            raise ValueError("Product ID cannot be empty.")
        if not self.__name:
            raise ValueError("Product name cannot be empty.")
        if self.__price < 0:
            raise ValueError("Price cannot be negative.")
        if self.__stock < 0:
            raise ValueError("Stock cannot be negative.")

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def display_supplier_information(self) -> None:
        self.__supplier.display_information()

    def update_stock(self, quantity: int) -> None:
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )
        self.display_supplier_information()

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return how this product is delivered to its customer."""

