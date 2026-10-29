"""Digital product implementation."""

from product import Product


class DigitalProduct(Product):
    """A product delivered digitally."""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = float(download_size)
        if self.__download_size < 0:
            raise ValueError("Download size cannot be negative.")

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"Type: Digital | Download size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self):
        return "This product is delivered digitally."

