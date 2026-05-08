import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from src.models import Order, Sample, Inventory, OrderStatus
from src.production_queue import ProductionJob
from src.json_production_queue import JsonProductionQueue
from src.production_service import ProductionService


@pytest.fixture
def mock_order_repo():
    return MagicMock()


@pytest.fixture
def mock_inventory_repo():
    return MagicMock()


@pytest.fixture
def sample():
    return Sample(sample_id="S001", name="GaN Wafer", avg_production_time=60, yield_rate=0.9)


@pytest.fixture
def producing_order():
    return Order(order_id="O001", sample_id="S001", customer_name="Lab", quantity=5, status=OrderStatus.PRODUCING)


def make_started_at(minutes_ago: float) -> str:
    return (datetime.now() - timedelta(minutes=minutes_ago)).isoformat()


class TestProductionServiceRestore:
    def test_restore_returns_empty_when_queue_is_empty(self, mock_order_repo, mock_inventory_repo, tmp_path):
        queue = JsonProductionQueue(str(tmp_path / "queue.json"))
        service = ProductionService(mock_order_repo, mock_inventory_repo, queue)
        result = service.restore()
        assert result == []

    def test_restore_completes_job_when_elapsed_exceeds_duration(
        self, mock_order_repo, mock_inventory_repo, tmp_path, producing_order, sample
    ):
        queue = JsonProductionQueue(str(tmp_path / "queue.json"))
        service = ProductionService(mock_order_repo, mock_inventory_repo, queue)

        job = queue.enqueue(producing_order, sample, shortage=5)
        # Manually set started_at to 999 minutes ago (well past duration)
        queue._jobs[0].started_at = make_started_at(999)
        queue._save()

        mock_order_repo.find_by_id.return_value = producing_order
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=0)

        completed = service.restore()
        assert len(completed) == 1
        assert completed[0].status == OrderStatus.CONFIRMED

    def test_restore_keeps_job_when_not_yet_elapsed(
        self, mock_order_repo, mock_inventory_repo, tmp_path, producing_order, sample
    ):
        queue = JsonProductionQueue(str(tmp_path / "queue.json"))
        service = ProductionService(mock_order_repo, mock_inventory_repo, queue)

        queue.enqueue(producing_order, sample, shortage=5)
        # started_at is just now → not elapsed

        completed = service.restore()
        assert completed == []
        assert queue.get_current_job() is not None

    def test_restore_completes_multiple_finished_jobs_in_order(
        self, mock_order_repo, mock_inventory_repo, tmp_path, producing_order, sample
    ):
        another = Order(order_id="O002", sample_id="S001", customer_name="Lab2", quantity=3, status=OrderStatus.PRODUCING)
        queue = JsonProductionQueue(str(tmp_path / "queue.json"))
        service = ProductionService(mock_order_repo, mock_inventory_repo, queue)

        queue.enqueue(producing_order, sample, shortage=5)
        queue.enqueue(another, sample, shortage=3)

        # Both jobs started long ago
        for job in queue._jobs:
            job.started_at = make_started_at(999)
        queue._save()

        mock_order_repo.find_by_id.side_effect = lambda oid: (
            producing_order if oid == "O001" else another
        )
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=0)

        completed = service.restore()
        assert len(completed) == 2
        assert queue.get_current_job() is None

    def test_restore_stops_at_first_incomplete_job(
        self, mock_order_repo, mock_inventory_repo, tmp_path, producing_order, sample
    ):
        another = Order(order_id="O002", sample_id="S001", customer_name="Lab2", quantity=3, status=OrderStatus.PRODUCING)
        queue = JsonProductionQueue(str(tmp_path / "queue.json"))
        service = ProductionService(mock_order_repo, mock_inventory_repo, queue)

        queue.enqueue(producing_order, sample, shortage=5)  # job1: not elapsed
        queue.enqueue(another, sample, shortage=3)            # job2: also not elapsed

        completed = service.restore()
        assert completed == []
        assert len(queue.list_all()) == 2
