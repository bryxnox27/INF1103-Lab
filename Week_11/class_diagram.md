# Week 11 Inventory System UML

The diagram extends the Week 10 model. An `Order` uses one discount strategy at a time; strategies can be shared across orders. The factory creates products but does not keep them. `Inventory` aggregates products, while `Order` composes its order lines.

```mermaid
classDiagram
    class Supplier {
        -supplier_id: String
        -name: String
        -contact_email: String
        +get_supplier_id(): String
        +get_name(): String
        +get_contact_email(): String
        +display_information(): None
    }
    class Product {
        <<abstract>>
        -product_id: String
        -name: String
        -price: float
        -stock: int
        -supplier: Supplier
        +get_product_id(): String
        +get_name(): String
        +get_price(): float
        +get_stock(): int
        +get_supplier(): Supplier
        +update_stock(quantity: int): None
        +get_fulfilment_info(): String
    }
    class PhysicalProduct {
        -weight: float
        +get_weight(): float
        +calculate_shipping_cost(): float
    }
    class DigitalProduct {
        -download_size: float
        +get_download_size(): float
    }
    class CanBeShipped {
        <<interface>>
        +calculate_shipping_cost(): float
    }
    class Inventory {
        -products: List~Product~
        +add_product(product: Product): bool
        +remove_product(product_id: String): bool
        +find_product(product_id: String): Product or None
        +update_stock(product_id: String, quantity: int): bool
        +display_all(): None
        +get_products(): List~Product~
    }
    class Order {
        -order_id: String
        -order_lines: List~OrderLine~
        -discount: DiscountStrategy
        +add_order_line(product: Product, quantity: int): None
        +remove_order_line(product_id: String): bool
        +set_discount(discount: DiscountStrategy): None
        +calculate_total(): float
    }
    class OrderLine {
        +product: Product
        +quantity: int
        +calculate_subtotal(): float
    }
    class DiscountStrategy {
        <<abstract>>
        +apply(total: float): float
    }
    class NoDiscount {
        +apply(total: float): float
    }
    class PercentageDiscount {
        -percentage: float
        +apply(total: float): float
    }
    class BulkDiscount {
        -threshold: float
        -amount: float
        +apply(total: float): float
    }
    class StudentDiscount {
        +apply(total: float): float
    }
    class ProductFactory {
        {static} +create(product_type: String, product_id: String, name: String, price: float, stock_quantity: int, supplier: Supplier, weight: float = 0.0, download_size: float = 0.0): Product
    }

    Product <|-- PhysicalProduct
    Product <|-- DigitalProduct
    CanBeShipped <|.. PhysicalProduct
    Supplier "1" <-- "0..*" Product : supplies
    Inventory "0..1" o-- "0..*" Product : aggregates
    Order "1" *-- "0..*" OrderLine : composes
    OrderLine "0..*" --> "1" Product : refers to
    Order "0..*" --> "1" DiscountStrategy : uses
    DiscountStrategy <|-- NoDiscount
    DiscountStrategy <|-- PercentageDiscount
    DiscountStrategy <|-- BulkDiscount
    DiscountStrategy <|-- StudentDiscount
    ProductFactory ..> Product : "«creates»"
```
