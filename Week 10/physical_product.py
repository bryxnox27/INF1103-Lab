"""Physical product implementation."""

from product import Product
from shipping import CanBeShipped
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped physically."""

    SHIPPING_RATE_PER_KG = 5.00

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        weight: float,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = float(weight)
        if self.__weight < 0:
            raise ValueError("Weight cannot be negative.")

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Physical | Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        """Calculate shipping at $5.00 per kilogram."""
        return self.__weight * self.SHIPPING_RATE_PER_KG

