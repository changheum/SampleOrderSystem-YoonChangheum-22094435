import pytest
from src.models import Sample, Order, Inventory, OrderStatus


class TestOrderStatus:
    def test_status_constants_exist(self):
        assert OrderStatus.RESERVED == "RESERVED"
        assert OrderStatus.REJECTED == "REJECTED"
        assert OrderStatus.PRODUCING == "PRODUCING"
        assert OrderStatus.CONFIRMED == "CONFIRMED"
        assert OrderStatus.RELEASE == "RELEASE"

    def test_all_statuses(self):
        all_statuses = OrderStatus.all()
        assert set(all_statuses) == {"RESERVED", "REJECTED", "PRODUCING", "CONFIRMED", "RELEASE"}


class TestSample:
    def test_create_valid_sample(self):
        sample = Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9)
        assert sample.sample_id == "S001"
        assert sample.name == "GaN Wafer"
        assert sample.avg_production_time == 120
        assert sample.yield_rate == 0.9

    def test_should_raise_when_avg_production_time_is_zero(self):
        with pytest.raises(ValueError, match="avg_production_time"):
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=0, yield_rate=0.9)

    def test_should_raise_when_avg_production_time_is_negative(self):
        with pytest.raises(ValueError, match="avg_production_time"):
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=-1, yield_rate=0.9)

    def test_should_raise_when_yield_rate_is_zero(self):
        with pytest.raises(ValueError, match="yield_rate"):
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.0)

    def test_should_raise_when_yield_rate_exceeds_one(self):
        with pytest.raises(ValueError, match="yield_rate"):
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=1.1)

    def test_yield_rate_of_one_is_valid(self):
        sample = Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=1.0)
        assert sample.yield_rate == 1.0

    def test_should_raise_when_sample_id_is_empty(self):
        with pytest.raises(ValueError, match="sample_id"):
            Sample(sample_id="", name="GaN Wafer", avg_production_time=120, yield_rate=0.9)

    def test_should_raise_when_name_is_empty(self):
        with pytest.raises(ValueError, match="name"):
            Sample(sample_id="S001", name="", avg_production_time=120, yield_rate=0.9)


class TestOrder:
    def test_create_valid_order(self):
        order = Order(
            order_id="O001",
            sample_id="S001",
            customer_name="KAIST Lab",
            quantity=10,
            status=OrderStatus.RESERVED,
        )
        assert order.order_id == "O001"
        assert order.status == "RESERVED"

    def test_should_raise_when_quantity_is_zero(self):
        with pytest.raises(ValueError, match="quantity"):
            Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=0, status=OrderStatus.RESERVED)

    def test_should_raise_when_quantity_is_negative(self):
        with pytest.raises(ValueError, match="quantity"):
            Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=-5, status=OrderStatus.RESERVED)

    def test_should_raise_when_status_is_invalid(self):
        with pytest.raises(ValueError, match="status"):
            Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=10, status="UNKNOWN")

    def test_should_raise_when_order_id_is_empty(self):
        with pytest.raises(ValueError, match="order_id"):
            Order(order_id="", sample_id="S001", customer_name="KAIST Lab", quantity=10, status=OrderStatus.RESERVED)

    def test_should_raise_when_customer_name_is_empty(self):
        with pytest.raises(ValueError, match="customer_name"):
            Order(order_id="O001", sample_id="S001", customer_name="", quantity=10, status=OrderStatus.RESERVED)

    def test_all_valid_statuses_are_accepted(self):
        for status in OrderStatus.all():
            order = Order(order_id="O001", sample_id="S001", customer_name="Lab", quantity=1, status=status)
            assert order.status == status


class TestInventory:
    def test_create_valid_inventory(self):
        inventory = Inventory(sample_id="S001", stock_quantity=100)
        assert inventory.sample_id == "S001"
        assert inventory.stock_quantity == 100

    def test_stock_quantity_of_zero_is_valid(self):
        inventory = Inventory(sample_id="S001", stock_quantity=0)
        assert inventory.stock_quantity == 0

    def test_should_raise_when_stock_quantity_is_negative(self):
        with pytest.raises(ValueError, match="stock_quantity"):
            Inventory(sample_id="S001", stock_quantity=-1)

    def test_should_raise_when_sample_id_is_empty(self):
        with pytest.raises(ValueError, match="sample_id"):
            Inventory(sample_id="", stock_quantity=10)
