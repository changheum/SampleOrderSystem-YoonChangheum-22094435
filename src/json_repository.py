import json
import os
from dataclasses import asdict
from src.models import Sample, Order, Inventory, OrderStatus
from src.repository import SampleRepository, OrderRepository, InventoryRepository


def _load(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _dump(file_path: str, data: dict) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class JsonSampleRepository(SampleRepository):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def save(self, sample: Sample) -> None:
        data = _load(self._file_path)
        data[sample.sample_id] = asdict(sample)
        _dump(self._file_path, data)

    def find_by_id(self, sample_id: str) -> Sample | None:
        record = _load(self._file_path).get(sample_id)
        return Sample(**record) if record else None

    def find_all(self) -> list[Sample]:
        return [Sample(**r) for r in _load(self._file_path).values()]

    def delete(self, sample_id: str) -> None:
        data = _load(self._file_path)
        data.pop(sample_id, None)
        _dump(self._file_path, data)


class JsonOrderRepository(OrderRepository):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def save(self, order: Order) -> None:
        data = _load(self._file_path)
        record = asdict(order)
        record["status"] = order.status.value
        data[order.order_id] = record
        _dump(self._file_path, data)

    def find_by_id(self, order_id: str) -> Order | None:
        record = _load(self._file_path).get(order_id)
        if not record:
            return None
        return Order(**{**record, "status": OrderStatus(record["status"])})

    def find_all(self) -> list[Order]:
        return [Order(**{**r, "status": OrderStatus(r["status"])}) for r in _load(self._file_path).values()]

    def delete(self, order_id: str) -> None:
        data = _load(self._file_path)
        data.pop(order_id, None)
        _dump(self._file_path, data)


class JsonInventoryRepository(InventoryRepository):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def save(self, inventory: Inventory) -> None:
        data = _load(self._file_path)
        data[inventory.sample_id] = asdict(inventory)
        _dump(self._file_path, data)

    def find_by_id(self, sample_id: str) -> Inventory | None:
        record = _load(self._file_path).get(sample_id)
        return Inventory(**record) if record else None

    def find_all(self) -> list[Inventory]:
        return [Inventory(**r) for r in _load(self._file_path).values()]

    def delete(self, sample_id: str) -> None:
        data = _load(self._file_path)
        data.pop(sample_id, None)
        _dump(self._file_path, data)
