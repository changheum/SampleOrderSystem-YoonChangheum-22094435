import pytest
from unittest.mock import MagicMock
from src.models import Order, OrderStatus
from src.release_service import ReleaseService


@pytest.fixture
def mock_order_repo():
    return MagicMock()


@pytest.fixture
def service(mock_order_repo):
    return ReleaseService(mock_order_repo)


@pytest.fixture
def confirmed_order():
    return Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=10, status=OrderStatus.CONFIRMED)


@pytest.fixture
def reserved_order():
    return Order(order_id="O002", sample_id="S001", customer_name="Lab", quantity=5, status=OrderStatus.RESERVED)


class TestReleaseServiceGetConfirmed:
    def test_returns_only_confirmed_orders(self, service, mock_order_repo, confirmed_order, reserved_order):
        mock_order_repo.find_all.return_value = [confirmed_order, reserved_order]
        result = service.get_confirmed_orders()
        assert len(result) == 1
        assert result[0].status == OrderStatus.CONFIRMED

    def test_returns_empty_when_no_confirmed_orders(self, service, mock_order_repo):
        mock_order_repo.find_all.return_value = []
        assert service.get_confirmed_orders() == []

    def test_returns_multiple_confirmed_orders(self, service, mock_order_repo):
        orders = [
            Order(order_id=f"O00{i}", sample_id="S001", customer_name="Lab", quantity=5, status=OrderStatus.CONFIRMED)
            for i in range(3)
        ]
        mock_order_repo.find_all.return_value = orders
        assert len(service.get_confirmed_orders()) == 3


class TestReleaseServiceRelease:
    def test_release_transitions_order_to_release_status(self, service, mock_order_repo, confirmed_order):
        mock_order_repo.find_by_id.return_value = confirmed_order
        result = service.release("O001")
        assert result.status == OrderStatus.RELEASE

    def test_release_saves_updated_order(self, service, mock_order_repo, confirmed_order):
        mock_order_repo.find_by_id.return_value = confirmed_order
        service.release("O001")
        saved = mock_order_repo.save.call_args[0][0]
        assert saved.status == OrderStatus.RELEASE
        assert saved.order_id == "O001"

    def test_release_preserves_order_data(self, service, mock_order_repo, confirmed_order):
        mock_order_repo.find_by_id.return_value = confirmed_order
        result = service.release("O001")
        assert result.sample_id == confirmed_order.sample_id
        assert result.customer_name == confirmed_order.customer_name
        assert result.quantity == confirmed_order.quantity

    def test_release_raises_when_order_not_found(self, service, mock_order_repo):
        mock_order_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Order"):
            service.release("NONEXISTENT")

    def test_release_raises_when_order_is_not_confirmed(self, service, mock_order_repo, reserved_order):
        mock_order_repo.find_by_id.return_value = reserved_order
        with pytest.raises(ValueError, match="CONFIRMED"):
            service.release("O002")

    def test_release_raises_for_producing_order(self, service, mock_order_repo):
        producing = Order(order_id="O003", sample_id="S001", customer_name="Lab", quantity=5, status=OrderStatus.PRODUCING)
        mock_order_repo.find_by_id.return_value = producing
        with pytest.raises(ValueError, match="CONFIRMED"):
            service.release("O003")

    def test_release_raises_for_already_released_order(self, service, mock_order_repo):
        released = Order(order_id="O004", sample_id="S001", customer_name="Lab", quantity=5, status=OrderStatus.RELEASE)
        mock_order_repo.find_by_id.return_value = released
        with pytest.raises(ValueError, match="CONFIRMED"):
            service.release("O004")
