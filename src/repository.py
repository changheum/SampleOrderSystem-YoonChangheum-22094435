from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def save(self, entity: T) -> None: ...

    @abstractmethod
    def find_by_id(self, entity_id: str) -> T | None: ...

    @abstractmethod
    def find_all(self) -> list[T]: ...

    @abstractmethod
    def delete(self, entity_id: str) -> None: ...


from src.models import Sample, Order, Inventory


class SampleRepository(BaseRepository[Sample]): ...
class OrderRepository(BaseRepository[Order]): ...
class InventoryRepository(BaseRepository[Inventory]): ...
