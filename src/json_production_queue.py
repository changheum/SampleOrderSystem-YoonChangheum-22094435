import json
import os
import uuid
from datetime import datetime
from src.models import Order, Sample
from src.production_calculator import ProductionCalculator
from src.production_queue import AbstractProductionQueue, ProductionJob


def _read_json_file(file_path: str) -> list:
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _to_record(job: ProductionJob) -> dict:
    return {
        "job_id": job.job_id,
        "order_id": job.order_id,
        "sample_id": job.sample_id,
        "target_quantity": job.target_quantity,
        "total_duration": job.total_duration,
        "produced_quantity": job.produced_quantity,
        "started_at": job.started_at,
    }


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
        self._reload()
        self._jobs.append(job)
        self._save()
        return job

    def get_current_job(self) -> ProductionJob | None:
        self._reload()
        return self._jobs[0] if self._jobs else None

    def get_waiting_jobs(self) -> list[ProductionJob]:
        self._reload()
        return self._jobs[1:]

    def list_all(self) -> list[ProductionJob]:
        self._reload()
        return list(self._jobs)

    def complete(self, job_id: str) -> ProductionJob:
        self._reload()
        if not self._jobs or self._jobs[0].job_id != job_id:
            raise ValueError(f"Job '{job_id}' not found as current job")
        job = self._jobs.pop(0)
        self._save()
        return job

    def _reload(self) -> None:
        self._jobs = self._load_jobs()

    def _load_jobs(self) -> list[ProductionJob]:
        return [ProductionJob(**r) for r in _read_json_file(self._file_path)]

    def _save(self) -> None:
        with open(self._file_path, "w", encoding="utf-8") as f:
            json.dump([_to_record(j) for j in self._jobs], f, ensure_ascii=False, indent=2)
