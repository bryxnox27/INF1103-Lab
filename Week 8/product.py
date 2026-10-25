"""Product class for the Week 8 inventory system."""


class Product:
    """Store the information and behavior for one product."""

    def __init__(self, product_id, name, price, stock):
        self.__product_id = str(product_id).strip()
        self.__name = str(name).strip()
        self.__price = float(price)
        self.__stock = int(stock)

        if self.__product_id == "":
            raise ValueError("Product ID cannot be empty.")
        if self.__name == "":
            raise ValueError("Product name cannot be empty.")
        if self.__price < 0:
            raise ValueError("Price cannot be negative.")
        if self.__stock < 0:
            raise ValueError("Stock cannot be negative.")

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        """Set the stock quantity after checking that it is valid."""
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = quantity

    def display_information(self):
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )
