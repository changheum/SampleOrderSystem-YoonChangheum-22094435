import os
import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
from src.models import Order, Sample, OrderStatus
from src.production_queue import ProductionJob
from src.json_production_queue import JsonProductionQueue


@pytest.fixture
def queue_file(tmp_path):
    return str(tmp_path / "queue.json")


@pytest.fixture
def sample():
    return Sample(sample_id="S001", name="GaN Wafer", avg_production_time=60, yield_rate=0.9)


@pytest.fixture
def producing_order():
    return Order(order_id="O001", sample_id="S001", customer_name="Lab", quantity=5, status=OrderStatus.PRODUCING)


@pytest.fixture
def another_order():
    return Order(order_id="O002", sample_id="S001", customer_name="Lab2", quantity=3, status=OrderStatus.PRODUCING)


class TestJsonProductionQueueEnqueue:
    def test_enqueue_adds_job_with_started_at(self, queue_file, producing_order, sample):
        queue = JsonProductionQueue(queue_file)
        job = queue.enqueue(producing_order, sample)
        assert job.started_at is not None
        datetime.fromisoformat(job.started_at)  # valid ISO format

    def test_enqueue_persists_to_file(self, queue_file, producing_order, sample):
        queue = JsonProductionQueue(queue_file)
        queue.enqueue(producing_order, sample)
        queue2 = JsonProductionQueue(queue_file)
        assert len(queue2.list_all()) == 1

    def test_enqueue_preserves_fifo_order(self, queue_file, producing_order, another_order, sample):
        queue = JsonProductionQueue(queue_file)
        queue.enqueue(producing_order, sample)
        queue.enqueue(another_order, sample)
        assert queue.get_current_job().order_id == "O001"

    def test_enqueue_with_shortage_calculates_correct_quantity(self, queue_file, producing_order, sample):
        queue = JsonProductionQueue(queue_file)
        job = queue.enqueue(producing_order, sample, shortage=5)
        # ceil(5 / (0.9 * 0.9)) = ceil(6.17) = 7
        assert job.target_quantity == 7


class TestJsonProductionQueueComplete:
    def test_complete_removes_job_and_persists(self, queue_file, producing_order, sample):
        queue = JsonProductionQueue(queue_file)
        job = queue.enqueue(producing_order, sample)
        queue.complete(job.job_id)
        queue2 = JsonProductionQueue(queue_file)
        assert queue2.get_current_job() is None

    def test_complete_raises_when_job_not_found(self, queue_file):
        queue = JsonProductionQueue(queue_file)
        with pytest.raises(ValueError, match="Job"):
            queue.complete("NONEXISTENT")

    def test_complete_advances_to_next_job(self, queue_file, producing_order, another_order, sample):
        queue = JsonProductionQueue(queue_file)
        j1 = queue.enqueue(producing_order, sample)
        queue.enqueue(another_order, sample)
        queue.complete(j1.job_id)
        assert queue.get_current_job().order_id == "O002"


class TestJsonProductionQueuePersistence:
    def test_load_restores_all_jobs(self, queue_file, producing_order, another_order, sample):
        queue1 = JsonProductionQueue(queue_file)
        queue1.enqueue(producing_order, sample)
        queue1.enqueue(another_order, sample)
        queue2 = JsonProductionQueue(queue_file)
        assert len(queue2.list_all()) == 2

    def test_load_restores_started_at(self, queue_file, producing_order, sample):
        queue1 = JsonProductionQueue(queue_file)
        job = queue1.enqueue(producing_order, sample)
        original_started_at = job.started_at
        queue2 = JsonProductionQueue(queue_file)
        assert queue2.get_current_job().started_at == original_started_at

    def test_empty_file_returns_empty_queue(self, queue_file):
        queue = JsonProductionQueue(queue_file)
        assert queue.list_all() == []
        assert queue.get_current_job() is None


class TestJsonProductionQueueFileSync:
    """데이터 파일 삭제 시 큐 상태가 즉시 반영되어야 한다 (file-sync)."""

    def test_get_current_job_returns_none_after_file_deleted(self, queue_file, producing_order, sample):
        queue = JsonProductionQueue(queue_file)
        queue.enqueue(producing_order, sample)
        os.remove(queue_file)
        assert queue.get_current_job() is None

    def test_list_all_returns_empty_after_file_deleted(self, queue_file, producing_order, another_order, sample):
        queue = JsonProductionQueue(queue_file)
        queue.enqueue(producing_order, sample)
        queue.enqueue(another_order, sample)
        os.remove(queue_file)
        assert queue.list_all() == []

    def test_get_waiting_jobs_returns_empty_after_file_deleted(self, queue_file, producing_order, another_order, sample):
        queue = JsonProductionQueue(queue_file)
        queue.enqueue(producing_order, sample)
        queue.enqueue(another_order, sample)
        os.remove(queue_file)
        assert queue.get_waiting_jobs() == []
