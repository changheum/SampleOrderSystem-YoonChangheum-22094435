import json
import os
import uuid
from datetime import datetime
from src.models import Order, Sample
from src.production_calculator import ProductionCalculator
from src.production_queue import AbstractProductionQueue, ProductionJob


def _load(file_path: str) -> list:
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


class JsonProductionQueue(AbstractProductionQueue):
    def __init__(self, file_path: str, calculator: ProductionCalculator = None):
        self._file_path = file_path
        self._calculator = calculator or ProductionCalculator()
        self._jobs: list[ProductionJob] = self._load_jobs()

    def enqueue(self, order: Order, sample: Sample, shortage: int = None) -> ProductionJob:
        actual_shortage = shortage if shortage is not None else order.quantity
        target_qty = self._calculator.calculate_quantity(actual_shortage, sample.yield_rate)
        duration = self._calculator.calculate_duration(sample.avg_production_time, target_qty)
        job = ProductionJob(
            job_id=str(uuid.uuid4()),
            order_id=order.order_id,
            sample_id=order.sample_id,
            target_quantity=target_qty,
            total_duration=duration,
            started_at=datetime.now().isoformat(),
        )
        self._jobs.append(job)
        self._save()
        return job

    def get_current_job(self) -> ProductionJob | None:
        return self._jobs[0] if self._jobs else None

    def get_waiting_jobs(self) -> list[ProductionJob]:
        return self._jobs[1:]

    def list_all(self) -> list[ProductionJob]:
        return list(self._jobs)

    def complete(self, job_id: str) -> ProductionJob:
        if not self._jobs or self._jobs[0].job_id != job_id:
            raise ValueError(f"Job '{job_id}' not found as current job")
        job = self._jobs.pop(0)
        self._save()
        return job

    def _load_jobs(self) -> list[ProductionJob]:
        return [ProductionJob(**r) for r in _load(self._file_path)]

    def _save(self) -> None:
        records = [
            {
                "job_id": j.job_id,
                "order_id": j.order_id,
                "sample_id": j.sample_id,
                "target_quantity": j.target_quantity,
                "total_duration": j.total_duration,
                "produced_quantity": j.produced_quantity,
                "started_at": j.started_at,
            }
            for j in self._jobs
        ]
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
