from src.protocols import ProductionQueueProtocol, ReadableOrderRepository, ReadableSampleRepository, ReadableInventoryRepository
from src.models import Order, Sample, Inventory, OrderStatus


class ConcreteQueue:
    def enqueue(self, order: Order, sample: Sample) -> None:
        pass


class ConcreteOrderReader:
    def find_all(self) -> list[Order]:
        return []


class ConcreteSampleReader:
    def find_all(self) -> list[Sample]:
        return []


class ConcreteInventoryReader:
    def find_by_id(self, entity_id: str) -> Inventory | None:
        return None


class TestProductionQueueProtocol:
    def test_concrete_class_satisfies_protocol(self):
        queue: ProductionQueueProtocol = ConcreteQueue()
        order = Order(order_id="O001", sample_id="S001", customer_name="Lab", quantity=5, status=OrderStatus.PRODUCING)
        sample = Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9)
        queue.enqueue(order, sample)


class TestReadableProtocols:
    def test_readable_order_repository_protocol(self):
        repo: ReadableOrderRepository = ConcreteOrderReader()
        assert repo.find_all() == []

    def test_readable_sample_repository_protocol(self):
        repo: ReadableSampleRepository = ConcreteSampleReader()
        assert repo.find_all() == []

    def test_readable_inventory_repository_protocol(self):
        repo: ReadableInventoryRepository = ConcreteInventoryReader()
        assert repo.find_by_id("S001") is None
