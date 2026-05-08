from typing import Protocol
from src.models import Order, Sample, Inventory


class ProductionQueueProtocol(Protocol):
    def enqueue(self, order: Order, sample: Sample) -> None: ...


class ReadableOrderRepository(Protocol):
    def find_all(self) -> list[Order]: ...


class ReadableSampleRepository(Protocol):
    def find_all(self) -> list[Sample]: ...


class ReadableInventoryRepository(Protocol):
    def find_by_id(self, entity_id: str) -> Inventory | None: ...
