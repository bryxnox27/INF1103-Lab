"""Inventory class for managing Product objects."""

from product import Product


class Inventory:
    """Store and manage a collection of products."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        product_id = str(product_id).strip()
        for product in self.__products:
            if product.get_product_id() == product_id:
                return product
        return None

    def update_stock(self, product_id, quantity):
        product = self.search_product(product_id)
        if product is None:
            return False
        product.update_stock(quantity)
        return True

    def display_all(self):
        print("\nCurrent Inventory")
        print("------------------------------------------------")
        if len(self.__products) == 0:
            print("No products in inventory.")
        else:
            for product in self.__products:
                product.display_information()
        print("------------------------------------------------")

    def get_products(self):
        products = []
        for product in self.__products:
            products.append(product)
        return products
