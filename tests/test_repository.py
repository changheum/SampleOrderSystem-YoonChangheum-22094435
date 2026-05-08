import json
import os
import pytest
from src.models import Sample, Order, Inventory, OrderStatus
from src.repository import SampleRepository, OrderRepository, InventoryRepository
from src.json_repository import JsonSampleRepository, JsonOrderRepository, JsonInventoryRepository


@pytest.fixture
def tmp_path_sample(tmp_path):
    return str(tmp_path / "samples.json")


@pytest.fixture
def tmp_path_order(tmp_path):
    return str(tmp_path / "orders.json")


@pytest.fixture
def tmp_path_inventory(tmp_path):
    return str(tmp_path / "inventories.json")


@pytest.fixture
def sample():
    return Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9)


@pytest.fixture
def another_sample():
    return Sample(sample_id="S002", name="SiC Chip", avg_production_time=60, yield_rate=0.8)


@pytest.fixture
def order():
    return Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=10, status=OrderStatus.RESERVED)


@pytest.fixture
def another_order():
    return Order(order_id="O002", sample_id="S001", customer_name="Samsung Lab", quantity=5, status=OrderStatus.CONFIRMED)


@pytest.fixture
def inventory():
    return Inventory(sample_id="S001", stock_quantity=100)


# ──────────────────────────────────────────────
# JsonSampleRepository
# ──────────────────────────────────────────────

class TestJsonSampleRepository:
    def test_save_creates_new_file_when_not_exists(self, tmp_path_sample, sample):
        repo = JsonSampleRepository(tmp_path_sample)
        repo.save(sample)
        assert os.path.exists(tmp_path_sample)

    def test_save_and_find_by_id_returns_same_sample(self, tmp_path_sample, sample):
        repo = JsonSampleRepository(tmp_path_sample)
        repo.save(sample)
        result = repo.find_by_id("S001")
        assert result.sample_id == sample.sample_id
        assert result.name == sample.name
        assert result.avg_production_time == sample.avg_production_time
        assert result.yield_rate == sample.yield_rate

    def test_find_by_id_returns_none_when_not_found(self, tmp_path_sample):
        repo = JsonSampleRepository(tmp_path_sample)
        assert repo.find_by_id("NONEXISTENT") is None

    def test_find_all_returns_empty_list_when_no_data(self, tmp_path_sample):
        repo = JsonSampleRepository(tmp_path_sample)
        assert repo.find_all() == []

    def test_find_all_returns_all_saved_samples(self, tmp_path_sample, sample, another_sample):
        repo = JsonSampleRepository(tmp_path_sample)
        repo.save(sample)
        repo.save(another_sample)
        results = repo.find_all()
        assert len(results) == 2

    def test_save_updates_existing_sample(self, tmp_path_sample, sample):
        repo = JsonSampleRepository(tmp_path_sample)
        repo.save(sample)
        updated = Sample(sample_id="S001", name="Updated Wafer", avg_production_time=200, yield_rate=0.95)
        repo.save(updated)
        result = repo.find_by_id("S001")
        assert result.name == "Updated Wafer"
        assert len(repo.find_all()) == 1

    def test_delete_removes_sample(self, tmp_path_sample, sample):
        repo = JsonSampleRepository(tmp_path_sample)
        repo.save(sample)
        repo.delete("S001")
        assert repo.find_by_id("S001") is None

    def test_delete_nonexistent_sample_does_not_raise(self, tmp_path_sample):
        repo = JsonSampleRepository(tmp_path_sample)
        repo.delete("NONEXISTENT")

    def test_data_persists_across_repository_instances(self, tmp_path_sample, sample):
        repo1 = JsonSampleRepository(tmp_path_sample)
        repo1.save(sample)
        repo2 = JsonSampleRepository(tmp_path_sample)
        result = repo2.find_by_id("S001")
        assert result.sample_id == "S001"


# ──────────────────────────────────────────────
# JsonOrderRepository
# ──────────────────────────────────────────────

class TestJsonOrderRepository:
    def test_save_and_find_by_id(self, tmp_path_order, order):
        repo = JsonOrderRepository(tmp_path_order)
        repo.save(order)
        result = repo.find_by_id("O001")
        assert result.order_id == "O001"
        assert result.status == OrderStatus.RESERVED

    def test_find_by_id_returns_none_when_not_found(self, tmp_path_order):
        repo = JsonOrderRepository(tmp_path_order)
        assert repo.find_by_id("NONEXISTENT") is None

    def test_find_all_returns_empty_list_initially(self, tmp_path_order):
        repo = JsonOrderRepository(tmp_path_order)
        assert repo.find_all() == []

    def test_find_all_returns_all_saved_orders(self, tmp_path_order, order, another_order):
        repo = JsonOrderRepository(tmp_path_order)
        repo.save(order)
        repo.save(another_order)
        assert len(repo.find_all()) == 2

    def test_save_updates_existing_order(self, tmp_path_order, order):
        repo = JsonOrderRepository(tmp_path_order)
        repo.save(order)
        updated = Order(order_id="O001", sample_id="S001", customer_name="KAIST Lab", quantity=10, status=OrderStatus.CONFIRMED)
        repo.save(updated)
        result = repo.find_by_id("O001")
        assert result.status == OrderStatus.CONFIRMED
        assert len(repo.find_all()) == 1

    def test_delete_removes_order(self, tmp_path_order, order):
        repo = JsonOrderRepository(tmp_path_order)
        repo.save(order)
        repo.delete("O001")
        assert repo.find_by_id("O001") is None

    def test_delete_nonexistent_order_does_not_raise(self, tmp_path_order):
        repo = JsonOrderRepository(tmp_path_order)
        repo.delete("NONEXISTENT")

    def test_order_status_is_preserved_as_enum(self, tmp_path_order, order):
        repo = JsonOrderRepository(tmp_path_order)
        repo.save(order)
        result = repo.find_by_id("O001")
        assert isinstance(result.status, OrderStatus)

    def test_data_persists_across_repository_instances(self, tmp_path_order, order):
        repo1 = JsonOrderRepository(tmp_path_order)
        repo1.save(order)
        repo2 = JsonOrderRepository(tmp_path_order)
        assert repo2.find_by_id("O001") is not None


# ──────────────────────────────────────────────
# JsonInventoryRepository
# ──────────────────────────────────────────────

class TestJsonInventoryRepository:
    def test_save_and_find_by_id(self, tmp_path_inventory, inventory):
        repo = JsonInventoryRepository(tmp_path_inventory)
        repo.save(inventory)
        result = repo.find_by_id("S001")
        assert result.sample_id == "S001"
        assert result.stock_quantity == 100

    def test_find_by_id_returns_none_when_not_found(self, tmp_path_inventory):
        repo = JsonInventoryRepository(tmp_path_inventory)
        assert repo.find_by_id("NONEXISTENT") is None

    def test_find_all_returns_empty_list_initially(self, tmp_path_inventory):
        repo = JsonInventoryRepository(tmp_path_inventory)
        assert repo.find_all() == []

    def test_save_updates_stock_quantity(self, tmp_path_inventory, inventory):
        repo = JsonInventoryRepository(tmp_path_inventory)
        repo.save(inventory)
        updated = Inventory(sample_id="S001", stock_quantity=50)
        repo.save(updated)
        result = repo.find_by_id("S001")
        assert result.stock_quantity == 50
        assert len(repo.find_all()) == 1

    def test_delete_removes_inventory(self, tmp_path_inventory, inventory):
        repo = JsonInventoryRepository(tmp_path_inventory)
        repo.save(inventory)
        repo.delete("S001")
        assert repo.find_by_id("S001") is None

    def test_delete_nonexistent_does_not_raise(self, tmp_path_inventory):
        repo = JsonInventoryRepository(tmp_path_inventory)
        repo.delete("NONEXISTENT")

    def test_data_persists_across_repository_instances(self, tmp_path_inventory, inventory):
        repo1 = JsonInventoryRepository(tmp_path_inventory)
        repo1.save(inventory)
        repo2 = JsonInventoryRepository(tmp_path_inventory)
        assert repo2.find_by_id("S001").stock_quantity == 100

    def test_save_and_find_inventory_with_zero_stock(self, tmp_path_inventory):
        repo = JsonInventoryRepository(tmp_path_inventory)
        repo.save(Inventory(sample_id="S001", stock_quantity=0))
        result = repo.find_by_id("S001")
        assert result.stock_quantity == 0


# ──────────────────────────────────────────────
# Corrupted JSON resilience
# ──────────────────────────────────────────────

class TestJsonResilienceOnCorruptedFile:
    def test_sample_repo_returns_empty_on_corrupted_file(self, tmp_path):
        bad_file = str(tmp_path / "bad.json")
        with open(bad_file, "w") as f:
            f.write("not valid json {{{")
        repo = JsonSampleRepository(bad_file)
        assert repo.find_all() == []
        assert repo.find_by_id("S001") is None

    def test_order_repo_returns_empty_on_corrupted_file(self, tmp_path):
        bad_file = str(tmp_path / "bad.json")
        with open(bad_file, "w") as f:
            f.write("not valid json {{{")
        repo = JsonOrderRepository(bad_file)
        assert repo.find_all() == []

    def test_inventory_repo_returns_empty_on_corrupted_file(self, tmp_path):
        bad_file = str(tmp_path / "bad.json")
        with open(bad_file, "w") as f:
            f.write("not valid json {{{")
        repo = JsonInventoryRepository(bad_file)
        assert repo.find_all() == []
