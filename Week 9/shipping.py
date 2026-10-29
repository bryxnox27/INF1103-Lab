"""Interface-style abstract base class for shippable items."""

from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Contract for objects that can calculate a shipping cost."""

    @abstractmethod
    def calculate_shipping_cost(self):
        """Return the shipping cost for this item."""

