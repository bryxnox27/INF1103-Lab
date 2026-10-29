"""Physical product implementation."""

from product import Product
from shipping import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped physically."""

    SHIPPING_RATE_PER_KG = 5.00

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)
        if self.__weight < 0:
            raise ValueError("Weight cannot be negative.")

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"Type: Physical | Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        """Calculate shipping at $5.00 per kilogram."""
        return self.__weight * self.SHIPPING_RATE_PER_KG

