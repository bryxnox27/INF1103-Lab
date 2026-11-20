"""Central place for creating concrete Product objects."""

from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    """Create a Product subclass from a product type and its saved fields."""

    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        *,
        weight: float = 0.0,
        download_size: float = 0.0,
    ) -> Product:
        kind = str(product_type).strip().lower()
        common = (
            product_id,
            name,
            float(price),
            int(stock_quantity),
            supplier,
        )
        if kind == "physical":
            return PhysicalProduct(*common, float(weight))
        if kind == "digital":
            return DigitalProduct(*common, float(download_size))
        raise ValueError(f"Unknown product type: {product_type}")
