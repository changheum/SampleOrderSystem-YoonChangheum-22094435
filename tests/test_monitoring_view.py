import pytest
from unittest.mock import patch
from src.models import Order, Sample, OrderStatus
from src.monitoring_service import InventoryStatusLabel
from src.views.monitoring_view import MonitoringView


@pytest.fixture
def view():
    return MonitoringView()


@pytest.fixture
def orders_by_status():
    return {
        OrderStatus.RESERVED: [
            Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=10, status=OrderStatus.RESERVED)
        ],
        OrderStatus.PRODUCING: [],
        OrderStatus.CONFIRMED: [],
        OrderStatus.RELEASE: [],
    }


@pytest.fixture
def inventory_entries():
    return [
        {
            "sample": Sample(sample_id="S001", name="GaN Wafer", avg_production_time=60, yield_rate=0.9),
            "stock_quantity": 100,
            "status": InventoryStatusLabel.SURPLUS,
        }
    ]


class TestMonitoringView:
    def test_show_orders_by_status_prints_reserved_order(self, view, orders_by_status, capsys):
        view.show_orders_by_status(orders_by_status)
        out = capsys.readouterr().out
        assert "KAIST Lab" in out
        assert "RESERVED" in out

    def test_show_orders_by_status_shows_empty_status(self, view, capsys):
        view.show_orders_by_status({OrderStatus.CONFIRMED: []})
        out = capsys.readouterr().out
        assert "CONFIRMED" in out
        assert "0건" in out

    def test_show_inventory_status_prints_sample_info(self, view, inventory_entries, capsys):
        view.show_inventory_status(inventory_entries)
        out = capsys.readouterr().out
        assert "GaN Wafer" in out
        assert "100" in out
        assert InventoryStatusLabel.SURPLUS in out

    def test_show_inventory_status_prints_empty_message(self, view, capsys):
        view.show_inventory_status([])
        assert "없습니다" in capsys.readouterr().out

    def test_show_error_prints_message(self, view, capsys):
        view.show_error("오류 발생")
        assert "오류 발생" in capsys.readouterr().out

    def test_show_menu_returns_choice(self, view):
        with patch("builtins.input", return_value="1"):
            assert view.show_menu() == "1"
