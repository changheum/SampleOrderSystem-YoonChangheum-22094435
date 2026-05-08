import pytest
from unittest.mock import MagicMock
from src.models import OrderStatus
from src.monitoring_service import InventoryStatusLabel
from src.controllers.monitoring_controller import MonitoringController


@pytest.fixture
def mock_service():
    return MagicMock()


@pytest.fixture
def mock_view():
    return MagicMock()


@pytest.fixture
def controller(mock_service, mock_view):
    return MonitoringController(mock_service, mock_view)


class TestMonitoringController:
    def test_show_orders_calls_service_and_view(self, controller, mock_service, mock_view):
        mock_service.get_orders_by_status.return_value = {
            OrderStatus.RESERVED: [], OrderStatus.PRODUCING: [],
            OrderStatus.CONFIRMED: [], OrderStatus.RELEASE: [],
        }
        controller.show_orders()
        mock_service.get_orders_by_status.assert_called_once()
        mock_view.show_orders_by_status.assert_called_once()

    def test_show_inventory_calls_service_and_view(self, controller, mock_service, mock_view):
        mock_service.get_inventory_status.return_value = []
        controller.show_inventory()
        mock_service.get_inventory_status.assert_called_once()
        mock_view.show_inventory_status.assert_called_once()

    def test_run_show_orders_then_exit(self, controller, mock_service, mock_view):
        mock_view.show_menu.side_effect = ["1", "3"]
        mock_service.get_orders_by_status.return_value = {
            OrderStatus.RESERVED: [], OrderStatus.PRODUCING: [],
            OrderStatus.CONFIRMED: [], OrderStatus.RELEASE: [],
        }
        controller.run()
        mock_service.get_orders_by_status.assert_called_once()

    def test_run_show_inventory_then_exit(self, controller, mock_service, mock_view):
        mock_view.show_menu.side_effect = ["2", "3"]
        mock_service.get_inventory_status.return_value = []
        controller.run()
        mock_service.get_inventory_status.assert_called_once()

    def test_run_invalid_choice_shows_error(self, controller, mock_service, mock_view):
        mock_view.show_menu.side_effect = ["9", "3"]
        controller.run()
        mock_view.show_error.assert_called_once()
