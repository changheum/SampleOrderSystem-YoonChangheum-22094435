import pytest
from unittest.mock import MagicMock
from src.models import Order, Sample, Inventory, OrderStatus
from src.production_service import ProductionService
from src.production_queue import ProductionQueue, ProductionJob


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
    return Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=10, status=OrderStatus.PRODUCING)


@pytest.fixture
def queue():
    return ProductionQueue()


@pytest.fixture
def service(mock_order_repo, mock_inventory_repo, queue):
    return ProductionService(mock_order_repo, mock_inventory_repo, queue)


class TestProductionQueue:
    def test_enqueue_adds_job(self, queue, producing_order, sample):
        queue.enqueue(producing_order, sample)
        assert len(queue.list_all()) == 1

    def test_enqueue_stores_correct_quantities(self, queue, producing_order, sample):
        queue.enqueue(producing_order, sample)
        job = queue.list_all()[0]
        # shortage=10, yield=0.9 → ceil(10/(0.9*0.9))=13
        assert job.target_quantity == 13
        assert job.produced_quantity == 0

    def test_enqueue_calculates_total_duration(self, queue, producing_order, sample):
        queue.enqueue(producing_order, sample)
        job = queue.list_all()[0]
        # avg_production_time=60, target_quantity=13 → 780
        assert job.total_duration == 780

    def test_fifo_order_is_preserved(self, queue, sample):
        order1 = Order(order_id="O001", sample_id="S001", customer_name="Lab1", quantity=5, status=OrderStatus.PRODUCING)
        order2 = Order(order_id="O002", sample_id="S001", customer_name="Lab2", quantity=3, status=OrderStatus.PRODUCING)
        queue.enqueue(order1, sample)
        queue.enqueue(order2, sample)
        assert queue.get_current_job().order_id == "O001"

    def test_get_current_job_returns_none_when_empty(self, queue):
        assert queue.get_current_job() is None

    def test_get_waiting_jobs_excludes_current(self, queue, sample):
        order1 = Order(order_id="O001", sample_id="S001", customer_name="Lab1", quantity=5, status=OrderStatus.PRODUCING)
        order2 = Order(order_id="O002", sample_id="S001", customer_name="Lab2", quantity=3, status=OrderStatus.PRODUCING)
        queue.enqueue(order1, sample)
        queue.enqueue(order2, sample)
        waiting = queue.get_waiting_jobs()
        assert len(waiting) == 1
        assert waiting[0].order_id == "O002"

    def test_list_all_returns_empty_when_no_jobs(self, queue):
        assert queue.list_all() == []

    def test_complete_removes_current_job(self, queue, sample):
        order = Order(order_id="O001", sample_id="S001", customer_name="Lab", quantity=5, status=OrderStatus.PRODUCING)
        queue.enqueue(order, sample)
        job_id = queue.get_current_job().job_id
        queue.complete(job_id)
        assert queue.get_current_job() is None

    def test_complete_raises_when_job_not_found(self, queue):
        with pytest.raises(ValueError, match="Job"):
            queue.complete("NONEXISTENT")

    def test_complete_advances_to_next_job(self, queue, sample):
        order1 = Order(order_id="O001", sample_id="S001", customer_name="Lab1", quantity=5, status=OrderStatus.PRODUCING)
        order2 = Order(order_id="O002", sample_id="S001", customer_name="Lab2", quantity=3, status=OrderStatus.PRODUCING)
        queue.enqueue(order1, sample)
        queue.enqueue(order2, sample)
        job_id = queue.get_current_job().job_id
        queue.complete(job_id)
        assert queue.get_current_job().order_id == "O002"


class TestProductionService:
    def test_enqueue_delegates_to_queue(self, service, mock_order_repo, mock_inventory_repo, producing_order, sample, queue):
        service.enqueue(producing_order, sample)
        assert len(queue.list_all()) == 1

    def test_get_current_job_returns_none_when_empty(self, service):
        assert service.get_current_job() is None

    def test_get_waiting_jobs_returns_empty_when_no_jobs(self, service):
        assert service.get_waiting_jobs() == []

    def test_complete_job_transitions_order_to_confirmed(self, service, mock_order_repo, mock_inventory_repo, producing_order, sample, queue):
        service.enqueue(producing_order, sample)
        job = service.get_current_job()
        mock_order_repo.find_by_id.return_value = producing_order
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=0)
        result = service.complete_job(job.job_id)
        assert result.status == OrderStatus.CONFIRMED

    def test_complete_job_updates_inventory(self, service, mock_order_repo, mock_inventory_repo, producing_order, sample, queue):
        service.enqueue(producing_order, sample)
        job = service.get_current_job()
        mock_order_repo.find_by_id.return_value = producing_order
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=5)
        service.complete_job(job.job_id)
        saved = mock_inventory_repo.save.call_args[0][0]
        # existing 5 + produced target_quantity(13) = 18
        assert saved.stock_quantity == 5 + job.target_quantity

    def test_complete_job_raises_when_order_not_found(self, service, mock_order_repo, producing_order, sample, queue):
        service.enqueue(producing_order, sample)
        job = service.get_current_job()
        mock_order_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Order"):
            service.complete_job(job.job_id)
