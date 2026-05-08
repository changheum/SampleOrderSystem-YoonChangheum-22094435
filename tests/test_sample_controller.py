import pytest
from unittest.mock import MagicMock, patch, call
from src.models import Sample, Inventory
from src.controllers.sample_controller import SampleController


@pytest.fixture
def mock_service():
    return MagicMock()


@pytest.fixture
def controller(mock_service):
    return SampleController(mock_service)


@pytest.fixture
def sample_entry():
    return {
        "sample": Sample(sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9),
        "stock_quantity": 50,
    }


class TestSampleControllerRegister:
    def test_register_calls_service_with_user_input(self, controller, mock_service):
        mock_service.register.return_value = Sample(
            sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9
        )
        inputs = iter(["S001", "GaN Wafer", "120", "0.9"])
        with patch("builtins.input", side_effect=inputs):
            controller.register()
        mock_service.register.assert_called_once_with(
            sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9
        )

    def test_register_prints_success_message(self, controller, mock_service, capsys):
        mock_service.register.return_value = Sample(
            sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9
        )
        inputs = iter(["S001", "GaN Wafer", "120", "0.9"])
        with patch("builtins.input", side_effect=inputs):
            controller.register()
        captured = capsys.readouterr()
        assert "S001" in captured.out

    def test_register_prints_error_on_duplicate(self, controller, mock_service, capsys):
        mock_service.register.side_effect = ValueError("already exists")
        inputs = iter(["S001", "GaN Wafer", "120", "0.9"])
        with patch("builtins.input", side_effect=inputs):
            controller.register()
        captured = capsys.readouterr()
        assert "already exists" in captured.out.lower() or "오류" in captured.out

    def test_register_prints_error_on_invalid_input(self, controller, mock_service, capsys):
        mock_service.register.side_effect = ValueError("avg_production_time must be greater than 0")
        inputs = iter(["S001", "GaN Wafer", "0", "0.9"])
        with patch("builtins.input", side_effect=inputs):
            controller.register()
        captured = capsys.readouterr()
        assert len(captured.out) > 0


class TestSampleControllerList:
    def test_list_displays_all_samples(self, controller, mock_service, sample_entry, capsys):
        mock_service.find_all.return_value = [sample_entry]
        controller.list_samples()
        captured = capsys.readouterr()
        assert "GaN Wafer" in captured.out
        assert "50" in captured.out

    def test_list_displays_message_when_empty(self, controller, mock_service, capsys):
        mock_service.find_all.return_value = []
        controller.list_samples()
        captured = capsys.readouterr()
        assert len(captured.out) > 0


class TestSampleControllerSearch:
    def test_search_displays_matching_results(self, controller, mock_service, sample_entry, capsys):
        mock_service.search_by_name.return_value = [sample_entry]
        with patch("builtins.input", return_value="GaN"):
            controller.search()
        captured = capsys.readouterr()
        assert "GaN Wafer" in captured.out

    def test_search_displays_message_when_no_results(self, controller, mock_service, capsys):
        mock_service.search_by_name.return_value = []
        with patch("builtins.input", return_value="Silicon"):
            controller.search()
        captured = capsys.readouterr()
        assert len(captured.out) > 0


class TestSampleControllerRun:
    def test_run_register_then_exit(self, controller, mock_service, capsys):
        mock_service.register.return_value = Sample(
            sample_id="S001", name="GaN Wafer", avg_production_time=120, yield_rate=0.9
        )
        menu_then_exit = iter(["1", "4"])
        field_inputs = iter(["S001", "GaN Wafer", "120", "0.9"])
        def fake_input(prompt=""):
            if "선택" in prompt:
                return next(menu_then_exit)
            return next(field_inputs)
        with patch("builtins.input", side_effect=fake_input):
            controller.run()

    def test_run_list_then_exit(self, controller, mock_service, capsys):
        mock_service.find_all.return_value = []
        inputs = iter(["2", "4"])
        with patch("builtins.input", side_effect=inputs):
            controller.run()

    def test_run_search_then_exit(self, controller, mock_service, capsys):
        mock_service.search_by_name.return_value = []
        inputs = iter(["3", "Silicon", "4"])
        with patch("builtins.input", side_effect=inputs):
            controller.run()
