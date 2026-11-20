"""Interchangeable order discount strategies."""

import math
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Common contract for objects that calculate a discounted total."""

    @abstractmethod
    def apply(self, total: float) -> float:
        """Return the total after applying this discount."""


class NoDiscount(DiscountStrategy):
    """Leave the order total unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Reduce a total by a percentage between zero and one hundred."""

    def __init__(self, percentage: float) -> None:
        self.__percentage = float(percentage)
        if not math.isfinite(self.__percentage) or not 0 <= self.__percentage <= 100:
            raise ValueError("Percentage must be finite and between 0 and 100.")

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Subtract a fixed amount when the total meets a threshold."""

    def __init__(self, threshold: float, amount: float) -> None:
        self.__threshold = float(threshold)
        self.__amount = float(amount)
        if not math.isfinite(self.__threshold) or self.__threshold < 0:
            raise ValueError("Threshold must be finite and nonnegative.")
        if not math.isfinite(self.__amount) or self.__amount < 0:
            raise ValueError("Discount amount must be finite and nonnegative.")

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(0.0, total - self.__amount)
        return total


class StudentDiscount(DiscountStrategy):
    """Apply a fixed five percent student discount."""

    def apply(self, total: float) -> float:
        return total * 0.95
