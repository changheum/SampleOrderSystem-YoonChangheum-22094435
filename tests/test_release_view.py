import pytest
from unittest.mock import patch
from src.models import Order, OrderStatus
from src.views.release_view import ReleaseView


@pytest.fixture
def view():
    return ReleaseView()


@pytest.fixture
def confirmed_orders():
    return [
        Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=10, status=OrderStatus.CONFIRMED),
        Order(order_id="O002", sample_id="S002", customer_name="Samsung Lab", quantity=5, status=OrderStatus.CONFIRMED),
    ]


class TestReleaseView:
    def test_show_confirmed_list_prints_order_info(self, view, confirmed_orders, capsys):
        view.show_confirmed_list(confirmed_orders)
        out = capsys.readouterr().out
        assert "KAIST Lab" in out
        assert "S001" in out

    def test_select_order_id_returns_input(self, view):
        with patch("builtins.input", return_value="O001"):
            assert view.select_order_id() == "O001"

    def test_show_release_success_prints_order_id(self, view, capsys):
        view.show_release_success("O001")
        assert "O001" in capsys.readouterr().out

    def test_show_error_prints_message(self, view, capsys):
        view.show_error("출고 불가")
        assert "출고 불가" in capsys.readouterr().out

    def test_show_menu_returns_choice(self, view):
        with patch("builtins.input", return_value="1"):
            assert view.show_menu() == "1"
