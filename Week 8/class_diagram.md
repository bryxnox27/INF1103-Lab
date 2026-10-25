# Week 8 UML Class Diagram

```mermaid
classDiagram
    class Product {
        - __product_id: String
        - __name: String
        - __price: float
        - __stock: int
        + __init__(product_id: String, name: String, price: float, stock: int): void
        + get_product_id(): String
        + get_name(): String
        + get_price(): float
        + get_stock(): int
        + update_stock(quantity: int): void
        + display_information(): void
    }

    class Inventory {
        - __products: List~Product~
        + __init__(): void
        + add_product(product: Product): bool
        + search_product(product_id: String): Product or None
        + update_stock(product_id: String, quantity: int): bool
        + display_all(): void
        + get_products(): List~Product~
    }

    Inventory "1" o-- "0..*" Product : contains
```

The main program creates and uses the `Inventory` and `Product` objects. JSON loading and saving remain in separate functions in `main.py`.
