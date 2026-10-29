# Week 9 UML Class Diagram

```mermaid
classDiagram
    class Product {
        <<abstract>>
        - __product_id: String
        - __name: String
        - __price: float
        - __stock: int
        + get_product_id(): String
        + get_name(): String
        + get_price(): float
        + get_stock(): int
        + update_stock(quantity: int): void
        + display_information(): void
        + get_fulfilment_info()*: String
    }
    class CanBeShipped {
        <<interface>>
        + calculate_shipping_cost()*: float
    }
    class PhysicalProduct {
        - __weight: float
        + get_weight(): float
        + display_information(): void
        + get_fulfilment_info(): String
        + calculate_shipping_cost(): float
    }
    class DigitalProduct {
        - __download_size: float
        + get_download_size(): float
        + display_information(): void
        + get_fulfilment_info(): String
    }
    class Inventory {
        - __products: List~Product~
        + add_product(product: Product): bool
        + search_product(product_id: String): Product or None
        + update_stock(product_id: String, quantity: int): bool
        + display_all(): void
        + get_products(): List~Product~
    }

    Product <|-- PhysicalProduct
    Product <|-- DigitalProduct
    CanBeShipped <|.. PhysicalProduct
    Inventory o-- "0..*" Product : manages
```

`PhysicalProduct` inherits common product behavior and fulfills the `CanBeShipped` interface contract. `DigitalProduct` does not implement shipping. `main.py` handles JSON loading and saving.
