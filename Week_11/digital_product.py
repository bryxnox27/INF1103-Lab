"""Digital product implementation."""

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A product delivered digitally."""

    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier,
        download_size: float,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__download_size: float = float(download_size)
        if self.__download_size < 0:
            raise ValueError("Download size cannot be negative.")

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"Type: Digital | Download size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."

