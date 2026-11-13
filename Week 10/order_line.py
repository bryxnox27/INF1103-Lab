"""One product and quantity within an order."""

from product import Product


class OrderLine:
    """A part owned by one Order; it refers to, but does not own, its Product."""

    def __init__(self, product: Product, quantity: int) -> None:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")

        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity
