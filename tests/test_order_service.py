import pytest
from unittest.mock import MagicMock, call
from src.models import Sample, Order, Inventory, OrderStatus
from src.order_service import OrderService


@pytest.fixture
def mock_order_repo():
    return MagicMock()


@pytest.fixture
def mock_sample_repo():
    return MagicMock()


@pytest.fixture
def mock_inventory_repo():
    return MagicMock()


@pytest.fixture
def mock_production_queue():
    return MagicMock()


@pytest.fixture
def service(mock_order_repo, mock_sample_repo, mock_inventory_repo, mock_production_queue):
    return OrderService(mock_order_repo, mock_sample_repo, mock_inventory_repo, mock_production_queue)


@pytest.fixture
def sample():
    return Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9)


@pytest.fixture
def reserved_order():
    return Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=10, status=OrderStatus.RESERVED)


@pytest.fixture
def inventory_sufficient():
    return Inventory(sample_id="S001", stock_quantity=100)


@pytest.fixture
def inventory_insufficient():
    return Inventory(sample_id="S001", stock_quantity=5)


@pytest.fixture
def inventory_empty():
    return Inventory(sample_id="S001", stock_quantity=0)


# ─────────────────────────────────────────────
# 주문 접수 (place_order)
# ─────────────────────────────────────────────

class TestOrderServicePlaceOrder:
    def test_place_order_creates_reserved_order(self, service, mock_order_repo, mock_sample_repo, sample):
        mock_sample_repo.find_by_id.return_value = sample
        result = service.place_order("S001", "KAIST Lab", 10)
        assert result.status == OrderStatus.RESERVED
        assert result.sample_id == "S001"
        assert result.customer_name == "KAIST Lab"
        assert result.quantity == 10
        mock_order_repo.save.assert_called_once()

    def test_place_order_raises_when_sample_not_found(self, service, mock_sample_repo):
        mock_sample_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Sample"):
            service.place_order("NONEXISTENT", "KAIST Lab", 10)

    def test_place_order_raises_when_quantity_is_zero(self, service, mock_sample_repo, sample):
        mock_sample_repo.find_by_id.return_value = sample
        with pytest.raises(ValueError):
            service.place_order("S001", "KAIST Lab", 0)

    def test_place_order_raises_when_quantity_is_negative(self, service, mock_sample_repo, sample):
        mock_sample_repo.find_by_id.return_value = sample
        with pytest.raises(ValueError):
            service.place_order("S001", "KAIST Lab", -1)


# ─────────────────────────────────────────────
# 주문 승인 — 재고 충분 (approve → CONFIRMED)
# ─────────────────────────────────────────────

class TestOrderServiceApproveWithSufficientStock:
    def test_approve_sets_status_to_confirmed_when_stock_sufficient(
        self, service, mock_order_repo, mock_sample_repo, mock_inventory_repo,
        reserved_order, sample, inventory_sufficient
    ):
        mock_order_repo.find_by_id.return_value = reserved_order
        mock_sample_repo.find_by_id.return_value = sample
        mock_inventory_repo.find_by_id.return_value = inventory_sufficient
        result = service.approve("O001")
        assert result.status == OrderStatus.CONFIRMED

    def test_approve_deducts_inventory_when_stock_sufficient(
        self, service, mock_order_repo, mock_sample_repo, mock_inventory_repo,
        reserved_order, sample, inventory_sufficient
    ):
        mock_order_repo.find_by_id.return_value = reserved_order
        mock_sample_repo.find_by_id.return_value = sample
        mock_inventory_repo.find_by_id.return_value = inventory_sufficient
        service.approve("O001")
        saved_inventory = mock_inventory_repo.save.call_args[0][0]
        assert saved_inventory.stock_quantity == 90  # 100 - 10

    def test_approve_with_exact_stock_sets_confirmed(
        self, service, mock_order_repo, mock_sample_repo, mock_inventory_repo,
        sample, reserved_order
    ):
        exact_inventory = Inventory(sample_id="S001", stock_quantity=10)
        mock_order_repo.find_by_id.return_value = reserved_order
        mock_sample_repo.find_by_id.return_value = sample
        mock_inventory_repo.find_by_id.return_value = exact_inventory
        result = service.approve("O001")
        assert result.status == OrderStatus.CONFIRMED
        saved_inventory = mock_inventory_repo.save.call_args[0][0]
        assert saved_inventory.stock_quantity == 0


# ─────────────────────────────────────────────
# 주문 승인 — 재고 부족 (approve → PRODUCING)
# ─────────────────────────────────────────────

class TestOrderServiceApproveWithInsufficientStock:
    def test_approve_sets_status_to_producing_when_stock_insufficient(
        self, service, mock_order_repo, mock_sample_repo, mock_inventory_repo, mock_production_queue,
        reserved_order, sample, inventory_insufficient
    ):
        mock_order_repo.find_by_id.return_value = reserved_order
        mock_sample_repo.find_by_id.return_value = sample
        mock_inventory_repo.find_by_id.return_value = inventory_insufficient
        result = service.approve("O001")
        assert result.status == OrderStatus.PRODUCING

    def test_approve_enqueues_production_when_stock_insufficient(
        self, service, mock_order_repo, mock_sample_repo, mock_inventory_repo, mock_production_queue,
        reserved_order, sample, inventory_insufficient
    ):
        mock_order_repo.find_by_id.return_value = reserved_order
        mock_sample_repo.find_by_id.return_value = sample
        mock_inventory_repo.find_by_id.return_value = inventory_insufficient
        service.approve("O001")
        mock_production_queue.enqueue.assert_called_once()

    def test_approve_sets_producing_when_stock_is_zero(
        self, service, mock_order_repo, mock_sample_repo, mock_inventory_repo, mock_production_queue,
        reserved_order, sample, inventory_empty
    ):
        mock_order_repo.find_by_id.return_value = reserved_order
        mock_sample_repo.find_by_id.return_value = sample
        mock_inventory_repo.find_by_id.return_value = inventory_empty
        result = service.approve("O001")
        assert result.status == OrderStatus.PRODUCING

    def test_approve_does_not_deduct_inventory_when_producing(
        self, service, mock_order_repo, mock_sample_repo, mock_inventory_repo, mock_production_queue,
        reserved_order, sample, inventory_insufficient
    ):
        mock_order_repo.find_by_id.return_value = reserved_order
        mock_sample_repo.find_by_id.return_value = sample
        mock_inventory_repo.find_by_id.return_value = inventory_insufficient
        service.approve("O001")
        mock_inventory_repo.save.assert_not_called()


# ─────────────────────────────────────────────
# 주문 승인 — 예외 케이스
# ─────────────────────────────────────────────

class TestOrderServiceApproveExceptions:
    def test_approve_raises_when_order_not_found(self, service, mock_order_repo):
        mock_order_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Order"):
            service.approve("NONEXISTENT")

    def test_approve_raises_when_order_is_not_reserved(self, service, mock_order_repo):
        confirmed_order = Order(
            order_id="O001", sample_id="S001", customer_name="Lab", quantity=10, status=OrderStatus.CONFIRMED
        )
        mock_order_repo.find_by_id.return_value = confirmed_order
        with pytest.raises(ValueError, match="RESERVED"):
            service.approve("O001")


# ─────────────────────────────────────────────
# 주문 거절 (reject)
# ─────────────────────────────────────────────

class TestOrderServiceReject:
    def test_reject_sets_status_to_rejected(self, service, mock_order_repo, reserved_order):
        mock_order_repo.find_by_id.return_value = reserved_order
        result = service.reject("O001")
        assert result.status == OrderStatus.REJECTED

    def test_reject_saves_updated_order(self, service, mock_order_repo, reserved_order):
        mock_order_repo.find_by_id.return_value = reserved_order
        service.reject("O001")
        saved = mock_order_repo.save.call_args[0][0]
        assert saved.status == OrderStatus.REJECTED

    def test_reject_raises_when_order_not_found(self, service, mock_order_repo):
        mock_order_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Order"):
            service.reject("NONEXISTENT")

    def test_reject_raises_when_order_is_not_reserved(self, service, mock_order_repo):
        producing_order = Order(
            order_id="O001", sample_id="S001", customer_name="Lab", quantity=10, status=OrderStatus.PRODUCING
        )
        mock_order_repo.find_by_id.return_value = producing_order
        with pytest.raises(ValueError, match="RESERVED"):
            service.reject("O001")


# ─────────────────────────────────────────────
# 예약 목록 조회 (find_reserved)
# ─────────────────────────────────────────────

class TestOrderServiceFindReserved:
    def test_find_reserved_returns_only_reserved_orders(self, service, mock_order_repo, reserved_order):
        confirmed = Order(order_id="O002", sample_id="S001", customer_name="Lab", quantity=5, status=OrderStatus.CONFIRMED)
        mock_order_repo.find_all.return_value = [reserved_order, confirmed]
        results = service.find_reserved()
        assert len(results) == 1
        assert results[0].status == OrderStatus.RESERVED

    def test_find_reserved_returns_empty_when_none(self, service, mock_order_repo):
        mock_order_repo.find_all.return_value = []
        assert service.find_reserved() == []
