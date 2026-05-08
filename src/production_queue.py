import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from collections import deque
from src.models import Order, Sample
from src.production_calculator import ProductionCalculator


@dataclass
class ProductionJob:
    job_id: str
    order_id: str
    sample_id: str
    target_quantity: int
    total_duration: int
    produced_quantity: int = field(default=0)


class AbstractProductionQueue(ABC):
    @abstractmethod
    def enqueue(self, order: Order, sample: Sample) -> ProductionJob: ...

    @abstractmethod
    def get_current_job(self) -> ProductionJob | None: ...

    @abstractmethod
    def get_waiting_jobs(self) -> list[ProductionJob]: ...

    @abstractmethod
    def list_all(self) -> list[ProductionJob]: ...

    @abstractmethod
    def complete(self, job_id: str) -> ProductionJob: ...


class ProductionQueue(AbstractProductionQueue):
    def __init__(self, calculator: ProductionCalculator = None):
        self._queue: deque[ProductionJob] = deque()
        self._calculator = calculator or ProductionCalculator()

    def enqueue(self, order: Order, sample: Sample) -> ProductionJob:
        target_qty = self._calculator.calculate_quantity(order.quantity, sample.yield_rate)
        duration = self._calculator.calculate_duration(sample.avg_production_time, target_qty)
        job = ProductionJob(
            job_id=str(uuid.uuid4()),
            order_id=order.order_id,
            sample_id=order.sample_id,
            target_quantity=target_qty,
            total_duration=duration,
        )
        self._queue.append(job)
        return job

    def get_current_job(self) -> ProductionJob | None:
        return self._queue[0] if self._queue else None

    def get_waiting_jobs(self) -> list[ProductionJob]:
        return list(self._queue)[1:]

    def list_all(self) -> list[ProductionJob]:
        return list(self._queue)

    def complete(self, job_id: str) -> ProductionJob:
        if not self._queue or self._queue[0].job_id != job_id:
            raise ValueError(f"Job '{job_id}' not found as current job")
        return self._queue.popleft()
