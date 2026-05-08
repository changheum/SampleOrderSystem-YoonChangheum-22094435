from dataclasses import dataclass


class OrderStatus:
    RESERVED = "RESERVED"
    REJECTED = "REJECTED"
    PRODUCING = "PRODUCING"
    CONFIRMED = "CONFIRMED"
    RELEASE = "RELEASE"

    @classmethod
    def all(cls) -> list:
        return [cls.RESERVED, cls.REJECTED, cls.PRODUCING, cls.CONFIRMED, cls.RELEASE]


@dataclass
class Sample:
    sample_id: str
    name: str
    avg_production_time: int
    yield_rate: float

    def __post_init__(self):
        if not self.sample_id:
            raise ValueError("sample_id must not be empty")
        if not self.name:
            raise ValueError("name must not be empty")
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
    status: str

    def __post_init__(self):
        if not self.order_id:
            raise ValueError("order_id must not be empty")
        if not self.customer_name:
            raise ValueError("customer_name must not be empty")
        if self.quantity <= 0:
            raise ValueError("quantity must be greater than 0")
        if self.status not in OrderStatus.all():
            raise ValueError(f"status '{self.status}' is not valid")


@dataclass
class Inventory:
    sample_id: str
    stock_quantity: int

    def __post_init__(self):
        if not self.sample_id:
            raise ValueError("sample_id must not be empty")
        if self.stock_quantity < 0:
            raise ValueError("stock_quantity must be 0 or greater")
