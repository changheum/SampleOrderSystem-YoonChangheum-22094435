import os
import json
import pytest
from src.data_reset_service import DataResetService


@pytest.fixture
def data_dir(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    return str(d)


@pytest.fixture
def service():
    return DataResetService()


class TestDataResetService:
    def test_reset_removes_all_json_files(self, service, data_dir):
        for name in ["samples.json", "orders.json", "inventories.json", "queue.json"]:
            path = os.path.join(data_dir, name)
            with open(path, "w") as f:
                json.dump({}, f)
        service.reset(data_dir)
        for name in ["samples.json", "orders.json", "inventories.json", "queue.json"]:
            assert not os.path.exists(os.path.join(data_dir, name))

    def test_reset_is_safe_when_files_do_not_exist(self, service, data_dir):
        service.reset(data_dir)  # should not raise

    def test_reset_removes_only_target_files(self, service, data_dir):
        keep_file = os.path.join(data_dir, "keep_me.txt")
        with open(keep_file, "w") as f:
            f.write("keep")
        service.reset(data_dir)
        assert os.path.exists(keep_file)

    def test_reset_returns_list_of_removed_files(self, service, data_dir):
        path = os.path.join(data_dir, "samples.json")
        with open(path, "w") as f:
            json.dump({}, f)
        removed = service.reset(data_dir)
        assert any("samples.json" in r for r in removed)

    def test_reset_returns_empty_list_when_nothing_to_remove(self, service, data_dir):
        removed = service.reset(data_dir)
        assert removed == []
