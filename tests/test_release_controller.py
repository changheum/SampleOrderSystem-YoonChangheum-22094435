import pytest
from unittest.mock import MagicMock
from src.models import Order, OrderStatus
from src.controllers.release_controller import ReleaseController


@pytest.fixture
def mock_service():
    return MagicMock()


@pytest.fixture
def mock_view():
    return MagicMock()


@pytest.fixture
def controller(mock_service, mock_view):
    return ReleaseController(mock_service, mock_view)


@pytest.fixture
def confirmed_order():
    return Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=10, status=OrderStatus.CONFIRMED)


@pytest.fixture
def released_order():
    return Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=10, status=OrderStatus.RELEASE)


class TestReleaseControllerRelease:
    def test_release_calls_service_with_selected_order_id(self, controller, mock_service, mock_view, confirmed_order, released_order):
        mock_service.get_confirmed_orders.return_value = [confirmed_order]
        mock_view.show_confirmed_list_and_select.return_value = "O001"
        mock_service.release.return_value = released_order
        controller.release()
        mock_service.release.assert_called_once_with("O001")

    def test_release_shows_success_message(self, controller, mock_service, mock_view, confirmed_order, released_order):
        mock_service.get_confirmed_orders.return_value = [confirmed_order]
        mock_view.show_confirmed_list_and_select.return_value = "O001"
        mock_service.release.return_value = released_order
        controller.release()
        mock_view.show_release_success.assert_called_once()

    def test_release_shows_error_when_no_confirmed_orders(self, controller, mock_service, mock_view):
        mock_service.get_confirmed_orders.return_value = []
        controller.release()
        mock_view.show_error.assert_called_once()
        mock_service.release.assert_not_called()

    def test_release_shows_error_on_service_exception(self, controller, mock_service, mock_view, confirmed_order):
        mock_service.get_confirmed_orders.return_value = [confirmed_order]
        mock_view.show_confirmed_list_and_select.return_value = "O001"
        mock_service.release.side_effect = ValueError("not CONFIRMED")
        controller.release()
        mock_view.show_error.assert_called_once()


class TestReleaseControllerRun:
    def test_run_release_then_exit(self, controller, mock_service, mock_view, confirmed_order, released_order):
        mock_view.show_menu.side_effect = ["1", "2"]
        mock_service.get_confirmed_orders.return_value = [confirmed_order]
        mock_view.show_confirmed_list_and_select.return_value = "O001"
        mock_service.release.return_value = released_order
        controller.run()
        mock_service.release.assert_called_once()

    def test_run_invalid_choice_shows_error(self, controller, mock_service, mock_view):
        mock_view.show_menu.side_effect = ["9", "2"]
        controller.run()
        mock_view.show_error.assert_called_once()

    def test_run_exits_on_choice_2(self, controller, mock_service, mock_view):
        mock_view.show_menu.return_value = "2"
        controller.run()
        mock_service.release.assert_not_called()
