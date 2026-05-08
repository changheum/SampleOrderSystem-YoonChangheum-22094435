from dataclasses import dataclass
from datetime import datetime, timedelta
from math import floor
from src.models import Order, Inventory, OrderStatus, Sample
from src.production_queue import AbstractProductionQueue, ProductionJob
from src.repository import OrderRepository, InventoryRepository


@dataclass
class ProductionProgress:
    job: ProductionJob
    produced_quantity: int
    estimated_completion: str


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

    def get_current_job_progress(self) -> ProductionProgress | None:
        job = self._queue.get_current_job()
        if job is None:
            return None
        return ProductionProgress(
            job=job,
            produced_quantity=self._calc_produced(job),
            estimated_completion=self._calc_completion(job),
        )

    def _calc_produced(self, job: ProductionJob) -> int:
        if not job.started_at:
            return 0
        elapsed = (datetime.now() - datetime.fromisoformat(job.started_at)).total_seconds() / 60
        return min(floor(job.target_quantity * elapsed / job.total_duration), job.target_quantity)

    def _calc_completion(self, job: ProductionJob) -> str:
        if not job.started_at:
            return "미정"
        return (datetime.fromisoformat(job.started_at) + timedelta(minutes=job.total_duration)).strftime("%Y-%m-%d %H:%M")

    def get_waiting_jobs(self) -> list[ProductionJob]:
        return self._queue.get_waiting_jobs()

    def complete_job(self, job_id: str) -> Order:
        job = self._queue.complete(job_id)
        order = self._order_repo.find_by_id(job.order_id)
        if order is None:
            raise ValueError(f"Order '{job.order_id}' not found")
        self._update_inventory(job, order.quantity)
        confirmed = Order(
            order_id=order.order_id,
            sample_id=order.sample_id,
            customer_name=order.customer_name,
            quantity=order.quantity,
            status=OrderStatus.CONFIRMED,
        )
        self._order_repo.save(confirmed)
        return confirmed

    def restore(self) -> list[Order]:
        completed = []
        while True:
            job = self._queue.get_current_job()
            if job is None or not job.started_at:
                break
            elapsed_minutes = (datetime.now() - datetime.fromisoformat(job.started_at)).total_seconds() / 60
            if elapsed_minutes >= job.total_duration:
                order = self.complete_job(job.job_id)
                completed.append(order)
            else:
                break
        return completed

    def _update_inventory(self, job: ProductionJob, order_quantity: int) -> None:
        existing = self._inventory_repo.find_by_id(job.sample_id)
        current_stock = existing.stock_quantity if existing else 0
        net_stock = current_stock + job.target_quantity - order_quantity
        updated = Inventory(sample_id=job.sample_id, stock_quantity=max(0, net_stock))
        self._inventory_repo.save(updated)
