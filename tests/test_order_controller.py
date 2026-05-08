import pytest
from unittest.mock import MagicMock, patch
from src.models import Order, Sample, Inventory, OrderStatus
from src.controllers.order_controller import OrderController


@pytest.fixture
def mock_service():
    return MagicMock()


@pytest.fixture
def mock_sample_service():
    return MagicMock()


@pytest.fixture
def mock_view():
    return MagicMock()


@pytest.fixture
def controller(mock_service, mock_sample_service, mock_view):
    return OrderController(mock_service, mock_sample_service, mock_view)


@pytest.fixture
def sample_entries():
    return [
        {
            "sample": Sample(sample_id="S001", name="GaN Wafer", avg_production_time=60, yield_rate=0.9),
            "stock_quantity": 50,
        }
    ]


@pytest.fixture
def reserved_order():
    return Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=10, status=OrderStatus.RESERVED)


class TestOrderControllerPlaceOrder:
    def test_place_order_shows_sample_list_before_prompt(self, controller, mock_service, mock_sample_service, mock_view, sample_entries):
        mock_sample_service.find_all.return_value = sample_entries
        mock_view.show_place_order_prompt.return_value = {"sample_id": "S001", "customer_name": "Lab", "quantity": "10"}
        mock_service.place_order.return_value = Order(
            order_id="O001", sample_id="S001", customer_name="Lab", quantity=10, status=OrderStatus.RESERVED
        )
        controller.place_order()
        calls = [c[0] for c in mock_view.method_calls]
        assert "show_sample_list_for_order" in calls
        assert "show_place_order_prompt" in calls
        assert calls.index("show_sample_list_for_order") < calls.index("show_place_order_prompt")

    def test_place_order_calls_service_with_user_input(self, controller, mock_service, mock_sample_service, mock_view, sample_entries):
        mock_sample_service.find_all.return_value = sample_entries
        mock_view.show_place_order_prompt.return_value = {"sample_id": "S001", "customer_name": "Lab", "quantity": "10"}
        mock_service.place_order.return_value = Order(
            order_id="O001", sample_id="S001", customer_name="Lab", quantity=10, status=OrderStatus.RESERVED
        )
        controller.place_order()
        mock_service.place_order.assert_called_once_with("S001", "Lab", 10)

    def test_place_order_shows_error_on_value_error(self, controller, mock_service, mock_sample_service, mock_view, sample_entries):
        mock_sample_service.find_all.return_value = sample_entries
        mock_view.show_place_order_prompt.return_value = {"sample_id": "NONE", "customer_name": "Lab", "quantity": "10"}
        mock_service.place_order.side_effect = ValueError("Sample not found")
        controller.place_order()
        mock_view.show_error.assert_called_once()

    def test_place_order_shows_error_when_no_samples_registered(self, controller, mock_service, mock_sample_service, mock_view):
        mock_sample_service.find_all.return_value = []
        controller.place_order()
        mock_view.show_error.assert_called_once()
        mock_service.place_order.assert_not_called()


class TestOrderControllerApproveReject:
    def test_approve_calls_service_approve(self, controller, mock_service, mock_view, reserved_order):
        mock_service.find_reserved.return_value = [reserved_order]
        mock_view.show_reserved_list_and_select.return_value = "O001"
        mock_view.show_approve_or_reject_prompt.return_value = "1"
        mock_service.approve.return_value = Order(
            order_id="O001", sample_id="S001", customer_name="Lab", quantity=10, status=OrderStatus.CONFIRMED
        )
        controller.approve_or_reject()
        mock_service.approve.assert_called_once_with("O001")

    def test_reject_calls_service_reject(self, controller, mock_service, mock_view, reserved_order):
        mock_service.find_reserved.return_value = [reserved_order]
        mock_view.show_reserved_list_and_select.return_value = "O001"
        mock_view.show_approve_or_reject_prompt.return_value = "2"
        mock_service.reject.return_value = Order(
            order_id="O001", sample_id="S001", customer_name="Lab", quantity=10, status=OrderStatus.REJECTED
        )
        controller.approve_or_reject()
        mock_service.reject.assert_called_once_with("O001")

    def test_approve_or_reject_shows_error_when_no_reserved_orders(self, controller, mock_service, mock_view):
        mock_service.find_reserved.return_value = []
        controller.approve_or_reject()
        mock_view.show_error.assert_called_once()

    def test_approve_or_reject_handles_service_error(self, controller, mock_service, mock_view, reserved_order):
        mock_service.find_reserved.return_value = [reserved_order]
        mock_view.show_reserved_list_and_select.return_value = "O001"
        mock_view.show_approve_or_reject_prompt.return_value = "1"
        mock_service.approve.side_effect = ValueError("already approved")
        controller.approve_or_reject()
        mock_view.show_error.assert_called_once()

    def test_approve_or_reject_shows_error_on_invalid_choice(self, controller, mock_service, mock_view, reserved_order):
        mock_service.find_reserved.return_value = [reserved_order]
        mock_view.show_reserved_list_and_select.return_value = "O001"
        mock_view.show_approve_or_reject_prompt.return_value = "9"
        controller.approve_or_reject()
        mock_service.approve.assert_not_called()
        mock_service.reject.assert_not_called()
        mock_view.show_error.assert_called_once()


class TestOrderControllerRun:
    def test_run_place_then_exit(self, controller, mock_service, mock_sample_service, mock_view, sample_entries):
        mock_view.show_menu.side_effect = ["1", "3"]
        mock_sample_service.find_all.return_value = sample_entries
        mock_view.show_place_order_prompt.return_value = {"sample_id": "S001", "customer_name": "Lab", "quantity": "5"}
        mock_service.place_order.return_value = Order(
            order_id="O001", sample_id="S001", customer_name="Lab", quantity=5, status=OrderStatus.RESERVED
        )
        controller.run()

    def test_run_approve_reject_then_exit(self, controller, mock_service, mock_view):
        mock_view.show_menu.side_effect = ["2", "3"]
        mock_service.find_reserved.return_value = []
        controller.run()

    def test_run_invalid_choice_then_exit(self, controller, mock_service, mock_view):
        mock_view.show_menu.side_effect = ["9", "3"]
        controller.run()
        mock_view.show_error.assert_called_once()
