from dataclasses import dataclass
from enum import Enum


class OrderStatus(str, Enum):
    RESERVED = "RESERVED"
    REJECTED = "REJECTED"
    PRODUCING = "PRODUCING"
    CONFIRMED = "CONFIRMED"
    RELEASE = "RELEASE"


def _require_non_blank(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must not be empty or blank")


@dataclass
class Sample:
    sample_id: str
    name: str
    avg_production_time: int
    yield_rate: float

    def __post_init__(self):
        _require_non_blank(self.sample_id, "sample_id")
        _require_non_blank(self.name, "name")
        if self.avg_production_time <= 0:
            raise ValueError("avg_production_time must be greater than 0")
        if not (0 < self.yield_rate <= 1):
            raise ValueError("yield_rate must be in range (0, 1]")


@dataclass
class Order:
    order_id: str
    sample_id: str
    customer_name: str
    quantity: int
    status: OrderStatus

    def __post_init__(self):
        _require_non_blank(self.order_id, "order_id")
        _require_non_blank(self.sample_id, "sample_id")
        _require_non_blank(self.customer_name, "customer_name")
        if self.quantity <= 0:
            raise ValueError("quantity must be greater than 0")
        if not isinstance(self.status, OrderStatus):
            raise ValueError(f"status '{self.status}' is not valid")


@dataclass
class Inventory:
    sample_id: str
    stock_quantity: int

    def __post_init__(self):
        _require_non_blank(self.sample_id, "sample_id")
        if self.stock_quantity < 0:
            raise ValueError("stock_quantity must be 0 or greater")
