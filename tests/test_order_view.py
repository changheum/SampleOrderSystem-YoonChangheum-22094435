import pytest
from unittest.mock import patch
from src.models import Order, OrderStatus
from src.views.order_view import OrderView


@pytest.fixture
def view():
    return OrderView()


@pytest.fixture
def reserved_orders():
    return [
        Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=10, status=OrderStatus.RESERVED),
        Order(order_id="O002", sample_id="S002", customer_name="Samsung Lab", quantity=5, status=OrderStatus.RESERVED),
    ]


class TestOrderView:
    def test_show_place_order_prompt_returns_input_dict(self, view):
        with patch("builtins.input", side_effect=["S001", "KAIST Lab", "10"]):
            result = view.show_place_order_prompt()
        assert result == {"sample_id": "S001", "customer_name": "KAIST Lab", "quantity": "10"}

    def test_show_place_order_success_prints_order_id(self, view, capsys):
        view.show_place_order_success("O001", "RESERVED")
        assert "O001" in capsys.readouterr().out

    def test_show_reserved_list_and_select_returns_selected_id(self, view, reserved_orders):
        with patch("builtins.input", return_value="O001"):
            result = view.show_reserved_list_and_select(reserved_orders)
        assert result == "O001"

    def test_show_reserved_list_prints_order_info(self, view, reserved_orders, capsys):
        with patch("builtins.input", return_value="O001"):
            view.show_reserved_list_and_select(reserved_orders)
        out = capsys.readouterr().out
        assert "KAIST Lab" in out
        assert "S001" in out

    def test_show_approve_or_reject_prompt_returns_choice(self, view):
        with patch("builtins.input", return_value="1"):
            result = view.show_approve_or_reject_prompt()
        assert result == "1"

    def test_show_approve_success_prints_status(self, view, capsys):
        view.show_approve_success("O001", "CONFIRMED")
        out = capsys.readouterr().out
        assert "O001" in out
        assert "CONFIRMED" in out

    def test_show_reject_success_prints_order_id(self, view, capsys):
        view.show_reject_success("O001")
        assert "O001" in capsys.readouterr().out

    def test_show_error_prints_message(self, view, capsys):
        view.show_error("something went wrong")
        assert "something went wrong" in capsys.readouterr().out

    def test_show_menu_returns_choice(self, view):
        with patch("builtins.input", return_value="2"):
            result = view.show_menu()
        assert result == "2"
