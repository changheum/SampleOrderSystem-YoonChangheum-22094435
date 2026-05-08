from abc import ABC, abstractmethod
from src.models import Sample, Order, Inventory


class SampleRepository(ABC):
    @abstractmethod
    def save(self, sample: Sample) -> None: ...

    @abstractmethod
    def find_by_id(self, sample_id: str) -> Sample | None: ...

    @abstractmethod
    def find_all(self) -> list[Sample]: ...

    @abstractmethod
    def delete(self, sample_id: str) -> None: ...


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None: ...

    @abstractmethod
    def find_by_id(self, order_id: str) -> Order | None: ...

    @abstractmethod
    def find_all(self) -> list[Order]: ...

    @abstractmethod
    def delete(self, order_id: str) -> None: ...


class InventoryRepository(ABC):
    @abstractmethod
    def save(self, inventory: Inventory) -> None: ...

    @abstractmethod
    def find_by_id(self, sample_id: str) -> Inventory | None: ...

    @abstractmethod
    def find_all(self) -> list[Inventory]: ...

    @abstractmethod
    def delete(self, sample_id: str) -> None: ...
