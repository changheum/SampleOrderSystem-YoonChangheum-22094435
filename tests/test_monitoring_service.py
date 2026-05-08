import pytest
from unittest.mock import MagicMock
from src.models import Order, Sample, Inventory, OrderStatus
from src.monitoring_service import MonitoringService, InventoryStatusLabel


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
def service(mock_order_repo, mock_sample_repo, mock_inventory_repo):
    return MonitoringService(mock_order_repo, mock_sample_repo, mock_inventory_repo)


def make_order(order_id, status, quantity=10):
    return Order(order_id=order_id, sample_id="S001", customer_name="Lab", quantity=quantity, status=status)


class TestMonitoringServiceOrdersByStatus:
    def test_returns_orders_grouped_by_status(self, service, mock_order_repo):
        mock_order_repo.find_all.return_value = [
            make_order("O001", OrderStatus.RESERVED),
            make_order("O002", OrderStatus.PRODUCING),
            make_order("O003", OrderStatus.CONFIRMED),
            make_order("O004", OrderStatus.RELEASE),
        ]
        result = service.get_orders_by_status()
        assert len(result[OrderStatus.RESERVED]) == 1
        assert len(result[OrderStatus.PRODUCING]) == 1
        assert len(result[OrderStatus.CONFIRMED]) == 1
        assert len(result[OrderStatus.RELEASE]) == 1

    def test_rejected_orders_are_excluded(self, service, mock_order_repo):
        mock_order_repo.find_all.return_value = [
            make_order("O001", OrderStatus.RESERVED),
            make_order("O002", OrderStatus.REJECTED),
        ]
        result = service.get_orders_by_status()
        assert OrderStatus.REJECTED not in result
        assert len(result[OrderStatus.RESERVED]) == 1

    def test_returns_empty_lists_when_no_orders(self, service, mock_order_repo):
        mock_order_repo.find_all.return_value = []
        result = service.get_orders_by_status()
        assert all(len(v) == 0 for v in result.values())
        assert OrderStatus.REJECTED not in result

    def test_multiple_orders_same_status(self, service, mock_order_repo):
        mock_order_repo.find_all.return_value = [
            make_order("O001", OrderStatus.RESERVED),
            make_order("O002", OrderStatus.RESERVED),
            make_order("O003", OrderStatus.CONFIRMED),
        ]
        result = service.get_orders_by_status()
        assert len(result[OrderStatus.RESERVED]) == 2
        assert len(result[OrderStatus.CONFIRMED]) == 1


class TestMonitoringServiceInventoryStatus:
    def test_returns_surplus_when_stock_exceeds_demand(self, service, mock_sample_repo, mock_order_repo, mock_inventory_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=60, yield_rate=0.9)
        ]
        mock_order_repo.find_all.return_value = [make_order("O001", OrderStatus.RESERVED, quantity=5)]
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=100)
        result = service.get_inventory_status()
        assert result[0]["status"] == InventoryStatusLabel.SURPLUS

    def test_returns_shortage_when_stock_below_demand(self, service, mock_sample_repo, mock_order_repo, mock_inventory_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=60, yield_rate=0.9)
        ]
        mock_order_repo.find_all.return_value = [make_order("O001", OrderStatus.RESERVED, quantity=50)]
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=10)
        result = service.get_inventory_status()
        assert result[0]["status"] == InventoryStatusLabel.SHORTAGE

    def test_returns_depleted_when_stock_is_zero(self, service, mock_sample_repo, mock_order_repo, mock_inventory_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=60, yield_rate=0.9)
        ]
        mock_order_repo.find_all.return_value = []
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=0)
        result = service.get_inventory_status()
        assert result[0]["status"] == InventoryStatusLabel.DEPLETED

    def test_rejected_orders_excluded_from_demand_calculation(self, service, mock_sample_repo, mock_order_repo, mock_inventory_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=60, yield_rate=0.9)
        ]
        mock_order_repo.find_all.return_value = [
            make_order("O001", OrderStatus.REJECTED, quantity=9999),
        ]
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=10)
        result = service.get_inventory_status()
        assert result[0]["status"] == InventoryStatusLabel.SURPLUS

    def test_returns_empty_when_no_samples(self, service, mock_sample_repo):
        mock_sample_repo.find_all.return_value = []
        assert service.get_inventory_status() == []

    def test_handles_missing_inventory_as_depleted(self, service, mock_sample_repo, mock_order_repo, mock_inventory_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=60, yield_rate=0.9)
        ]
        mock_order_repo.find_all.return_value = []
        mock_inventory_repo.find_by_id.return_value = None
        result = service.get_inventory_status()
        assert result[0]["status"] == InventoryStatusLabel.DEPLETED

    def test_inventory_status_includes_stock_quantity(self, service, mock_sample_repo, mock_order_repo, mock_inventory_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=60, yield_rate=0.9)
        ]
        mock_order_repo.find_all.return_value = []
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=42)
        result = service.get_inventory_status()
        assert result[0]["stock_quantity"] == 42
        assert result[0]["sample"].name == "GaN Wafer"

    def test_returns_surplus_when_stock_equals_demand(self, service, mock_sample_repo, mock_order_repo, mock_inventory_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=60, yield_rate=0.9)
        ]
        mock_order_repo.find_all.return_value = [make_order("O001", OrderStatus.RESERVED, quantity=10)]
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=10)
        result = service.get_inventory_status()
        assert result[0]["status"] == InventoryStatusLabel.SURPLUS
