"""Orders compose and manage their own order lines."""

from order_line import OrderLine
from product import Product


class Order:
    """An order owns the lifecycle of the OrderLine objects it creates."""

    def __init__(self, order_id: str) -> None:
        self.order_id: str = str(order_id).strip()
        if not self.order_id:
            raise ValueError("Order ID cannot be empty.")
        self.__order_lines: list[OrderLine] = []

    @property
    def order_lines(self) -> list[OrderLine]:
        """Return a copy so callers cannot move lines between orders."""
        return self.__order_lines.copy()

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        """Remove the first line for a product; the Order remains its manager."""
        product_id = str(product_id).strip()
        for index, order_line in enumerate(self.__order_lines):
            if order_line.product.get_product_id() == product_id:
                del self.__order_lines[index]
                return True
        return False

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_order_lines(self) -> None:
        print(f"\nOrder {self.order_id}")
        if not self.__order_lines:
            print("No order lines.")
            return

        for order_line in self.__order_lines:
            product = order_line.product
            print(
                f"{product.get_product_id()} | {product.get_name()} | "
                f"{order_line.quantity} x ${product.get_price():.2f} = "
                f"${order_line.calculate_subtotal():.2f}"
            )
        print(f"Order total: ${self.calculate_total():.2f}")
