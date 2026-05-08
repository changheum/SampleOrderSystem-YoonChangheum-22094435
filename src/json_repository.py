import json
import os
from src.models import Sample, Order, Inventory, OrderStatus
from src.repository import SampleRepository, OrderRepository, InventoryRepository


def _load(file_path: str) -> dict:
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _dump(file_path: str, data: dict) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


class JsonSampleRepository(SampleRepository):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def save(self, sample: Sample) -> None:
        data = _load(self._file_path)
        data[sample.sample_id] = {
            "sample_id": sample.sample_id,
            "name": sample.name,
            "avg_production_time": sample.avg_production_time,
            "yield_rate": sample.yield_rate,
        }
        _dump(self._file_path, data)

    def find_by_id(self, sample_id: str) -> Sample | None:
        data = _load(self._file_path)
        record = data.get(sample_id)
        return Sample(**record) if record else None

    def find_all(self) -> list[Sample]:
        data = _load(self._file_path)
        return [Sample(**record) for record in data.values()]

    def delete(self, sample_id: str) -> None:
        data = _load(self._file_path)
        data.pop(sample_id, None)
        _dump(self._file_path, data)


class JsonOrderRepository(OrderRepository):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def save(self, order: Order) -> None:
        data = _load(self._file_path)
        data[order.order_id] = {
            "order_id": order.order_id,
            "sample_id": order.sample_id,
            "customer_name": order.customer_name,
            "quantity": order.quantity,
            "status": order.status.value,
        }
        _dump(self._file_path, data)

    def find_by_id(self, order_id: str) -> Order | None:
        data = _load(self._file_path)
        record = data.get(order_id)
        if not record:
            return None
        return Order(**{**record, "status": OrderStatus(record["status"])})

    def find_all(self) -> list[Order]:
        data = _load(self._file_path)
        return [Order(**{**r, "status": OrderStatus(r["status"])}) for r in data.values()]

    def delete(self, order_id: str) -> None:
        data = _load(self._file_path)
        data.pop(order_id, None)
        _dump(self._file_path, data)


class JsonInventoryRepository(InventoryRepository):
    def __init__(self, file_path: str):
        self._file_path = file_path

    def save(self, inventory: Inventory) -> None:
        data = _load(self._file_path)
        data[inventory.sample_id] = {
            "sample_id": inventory.sample_id,
            "stock_quantity": inventory.stock_quantity,
        }
        _dump(self._file_path, data)

    def find_by_id(self, sample_id: str) -> Inventory | None:
        data = _load(self._file_path)
        record = data.get(sample_id)
        return Inventory(**record) if record else None

    def find_all(self) -> list[Inventory]:
        data = _load(self._file_path)
        return [Inventory(**record) for record in data.values()]

    def delete(self, sample_id: str) -> None:
        data = _load(self._file_path)
        data.pop(sample_id, None)
        _dump(self._file_path, data)
