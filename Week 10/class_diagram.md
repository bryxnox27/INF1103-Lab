# Week 10 UML Class Diagram

```mermaid
classDiagram
    class Supplier {
        - supplier_id: str
        - name: str
        - contact_email: str
        + get_supplier_id(): str
        + get_name(): str
        + get_contact_email(): str
        + display_information(): None
    }
    class Product {
        <<abstract>>
        - product_id: str
        - name: str
        - price: float
        - stock: int
        - supplier: Supplier
        + get_product_id(): str
        + get_name(): str
        + get_price(): float
        + get_stock(): int
        + get_supplier(): Supplier
        + update_stock(quantity: int): None
        + display_information(): None
        + get_fulfilment_info(): str*
    }
    class CanBeShipped {
        <<interface>>
        + calculate_shipping_cost(): float*
    }
    class PhysicalProduct {
        - weight: float
        + get_weight(): float
        + display_information(): None
        + get_fulfilment_info(): str
        + calculate_shipping_cost(): float
    }
    class DigitalProduct {
        - download_size: float
        + get_download_size(): float
        + display_information(): None
        + get_fulfilment_info(): str
    }
    class Inventory {
        - products: list~Product~
        + add_product(product: Product): bool
        + remove_product(product_id: str): bool
        + find_product(product_id: str): Product or None
        + update_stock(product_id: str, quantity: int): bool
        + display_all(): None
        + get_products(): list~Product~
    }
    class Order {
        - order_id: str
        - order_lines: list~OrderLine~
        + add_order_line(product: Product, quantity: int): None
        + remove_order_line(product_id: str): bool
        + calculate_total(): float
        + display_order_lines(): None
    }
    class OrderLine {
        + product: Product
        + quantity: int
        + calculate_subtotal(): float
    }

    Product <|-- PhysicalProduct
    Product <|-- DigitalProduct
    CanBeShipped <|.. PhysicalProduct
    Supplier "1" <-- "0..*" Product : supplied by
    Inventory "0..1" o-- "0..*" Product : aggregates
    Order "1" *-- "0..*" OrderLine : composes
    OrderLine "0..*" --> "1" Product : references
```

`Supplier` and `Product` are associated, so each product can refer to one supplier while both objects have independent lifecycles. `Inventory` aggregates products: a product can exist outside an inventory and can be transferred. `Order` composes order lines: an order creates and manages its lines. Each order line refers to a product without owning it.

`Inventory` stores the abstract `Product` type. Its normal product operations call shared methods, so `PhysicalProduct` and `DigitalProduct` work through the same collection. `CanBeShipped` describes a capability implemented by physical products.
