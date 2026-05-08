import pytest
from unittest.mock import MagicMock
from src.models import Sample, Inventory, OrderStatus
from src.sample_service import SampleService


@pytest.fixture
def mock_sample_repo():
    return MagicMock()


@pytest.fixture
def mock_inventory_repo():
    return MagicMock()


@pytest.fixture
def service(mock_sample_repo, mock_inventory_repo):
    return SampleService(mock_sample_repo, mock_inventory_repo)


@pytest.fixture
def sample():
    return Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9)


class TestSampleServiceRegister:
    def test_register_saves_sample_and_creates_inventory(self, service, mock_sample_repo, mock_inventory_repo):
        mock_sample_repo.find_by_id.return_value = None
        result = service.register("S001", "GaN Wafer", 120, 0.9)
        mock_sample_repo.save.assert_called_once()
        mock_inventory_repo.save.assert_called_once()
        assert result.sample_id == "S001"
        assert result.name == "GaN Wafer"

    def test_register_initial_inventory_is_zero(self, service, mock_sample_repo, mock_inventory_repo):
        mock_sample_repo.find_by_id.return_value = None
        service.register("S001", "GaN Wafer", 120, 0.9)
        saved_inventory = mock_inventory_repo.save.call_args[0][0]
        assert saved_inventory.stock_quantity == 0

    def test_should_raise_when_sample_id_already_exists(self, service, mock_sample_repo, sample):
        mock_sample_repo.find_by_id.return_value = sample
        with pytest.raises(ValueError, match="already exists"):
            service.register("S001", "GaN Wafer", 120, 0.9)

    def test_should_raise_when_yield_rate_is_invalid(self, service, mock_sample_repo):
        mock_sample_repo.find_by_id.return_value = None
        with pytest.raises(ValueError):
            service.register("S001", "GaN Wafer", 120, 1.5)

    def test_should_raise_when_avg_production_time_is_zero(self, service, mock_sample_repo):
        mock_sample_repo.find_by_id.return_value = None
        with pytest.raises(ValueError):
            service.register("S001", "GaN Wafer", 0, 0.9)


class TestSampleServiceFindAll:
    def test_find_all_returns_samples_with_inventory(self, service, mock_sample_repo, mock_inventory_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9),
            Sample(sample_id="S002", name="SiC Chip", avg_production_time=60, yield_rate=0.8),
        ]
        mock_inventory_repo.find_by_id.side_effect = lambda sid: (
            Inventory(sample_id=sid, stock_quantity=50 if sid == "S001" else 0)
        )
        results = service.find_all()
        assert len(results) == 2
        assert results[0]["stock_quantity"] == 50
        assert results[1]["stock_quantity"] == 0

    def test_find_all_returns_empty_when_no_samples(self, service, mock_sample_repo):
        mock_sample_repo.find_all.return_value = []
        assert service.find_all() == []

    def test_find_all_handles_missing_inventory(self, service, mock_sample_repo, mock_inventory_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9),
        ]
        mock_inventory_repo.find_by_id.return_value = None
        results = service.find_all()
        assert results[0]["stock_quantity"] == 0


class TestSampleServiceSearch:
    def test_search_by_name_returns_matching_samples(self, service, mock_sample_repo, mock_inventory_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9),
            Sample(sample_id="S002", name="SiC Chip", avg_production_time=60, yield_rate=0.8),
        ]
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=10)
        results = service.search_by_name("GaN")
        assert len(results) == 1
        assert results[0]["sample"].name == "GaN Wafer"

    def test_search_by_name_is_case_insensitive(self, service, mock_sample_repo, mock_inventory_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9),
        ]
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=5)
        assert len(service.search_by_name("gan")) == 1
        assert len(service.search_by_name("GAN")) == 1

    def test_search_by_name_returns_empty_when_no_match(self, service, mock_sample_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9),
        ]
        assert service.search_by_name("Silicon") == []

    def test_search_by_name_with_empty_keyword_returns_all(self, service, mock_sample_repo, mock_inventory_repo):
        mock_sample_repo.find_all.return_value = [
            Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9),
            Sample(sample_id="S002", name="SiC Chip", avg_production_time=60, yield_rate=0.8),
        ]
        mock_inventory_repo.find_by_id.return_value = Inventory(sample_id="S001", stock_quantity=0)
        assert len(service.search_by_name("")) == 2
