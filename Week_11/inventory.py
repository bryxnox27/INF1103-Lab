"""Inventory class for managing Product objects."""

from product import Product


class Inventory:
    """Store and manage a collection of products."""

    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        product_id = str(product_id).strip()
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        """Compatibility alias retained for the Week 9 command-line app."""
        return self.find_product(product_id)

    def update_stock(self, product_id: str, quantity: int) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        product.update_stock(quantity)
        return True

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("------------------------------------------------")
        if len(self.__products) == 0:
            print("No products in inventory.")
        else:
            for product in self.__products:
                product.display_information()
        print("------------------------------------------------")

    def get_products(self) -> list[Product]:
        return self.__products.copy()
