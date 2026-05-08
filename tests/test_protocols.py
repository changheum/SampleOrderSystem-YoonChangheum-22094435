from src.protocols import ProductionQueueProtocol
from src.models import Order, Sample, OrderStatus


class ConcreteQueue:
    def enqueue(self, order: Order, sample: Sample) -> None:
        pass


class TestProductionQueueProtocol:
    def test_concrete_class_satisfies_protocol(self):
        queue: ProductionQueueProtocol = ConcreteQueue()
        order = Order(order_id="O001", sample_id="S001", customer_name="Lab", quantity=5, status=OrderStatus.PRODUCING)
        sample = Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9)
        queue.enqueue(order, sample)
