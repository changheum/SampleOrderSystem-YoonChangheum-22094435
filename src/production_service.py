from src.models import Order, Inventory, OrderStatus, Sample
from src.production_queue import AbstractProductionQueue, ProductionJob
from src.repository import OrderRepository, InventoryRepository


class ProductionService:
    def __init__(
        self,
        order_repo: OrderRepository,
        inventory_repo: InventoryRepository,
        production_queue: AbstractProductionQueue,
    ):
        self._order_repo = order_repo
        self._inventory_repo = inventory_repo
        self._queue = production_queue

    def enqueue(self, order: Order, sample: Sample) -> ProductionJob:
        return self._queue.enqueue(order, sample)

    def get_current_job(self) -> ProductionJob | None:
        return self._queue.get_current_job()

    def get_waiting_jobs(self) -> list[ProductionJob]:
        return self._queue.get_waiting_jobs()

    def complete_job(self, job_id: str) -> Order:
        job = self._queue.complete(job_id)
        order = self._order_repo.find_by_id(job.order_id)
        if order is None:
            raise ValueError(f"Order '{job.order_id}' not found")
        self._update_inventory(job)
        confirmed = Order(
            order_id=order.order_id,
            sample_id=order.sample_id,
            customer_name=order.customer_name,
            quantity=order.quantity,
            status=OrderStatus.CONFIRMED,
        )
        self._order_repo.save(confirmed)
        return confirmed

    def _update_inventory(self, job: ProductionJob) -> None:
        existing = self._inventory_repo.find_by_id(job.sample_id)
        current_stock = existing.stock_quantity if existing else 0
        updated = Inventory(sample_id=job.sample_id, stock_quantity=current_stock + job.target_quantity)
        self._inventory_repo.save(updated)
