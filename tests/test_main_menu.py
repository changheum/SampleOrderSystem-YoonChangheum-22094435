import pytest
from unittest.mock import MagicMock
from src.main_menu import MainMenu


@pytest.fixture
def mock_sample_ctrl():
    return MagicMock()


@pytest.fixture
def mock_order_ctrl():
    return MagicMock()


@pytest.fixture
def mock_monitoring_ctrl():
    return MagicMock()


@pytest.fixture
def mock_production_ctrl():
    return MagicMock()


@pytest.fixture
def mock_release_ctrl():
    return MagicMock()


@pytest.fixture
def mock_reset_svc():
    return MagicMock()


@pytest.fixture
def mock_view():
    return MagicMock()


@pytest.fixture
def menu(mock_sample_ctrl, mock_order_ctrl, mock_monitoring_ctrl, mock_production_ctrl, mock_release_ctrl, mock_reset_svc, mock_view):
    return MainMenu(
        sample_ctrl=mock_sample_ctrl,
        order_ctrl=mock_order_ctrl,
        monitoring_ctrl=mock_monitoring_ctrl,
        production_ctrl=mock_production_ctrl,
        release_ctrl=mock_release_ctrl,
        reset_svc=mock_reset_svc,
        view=mock_view,
    )


class TestMainMenuRun:
    def test_choice_1_runs_sample_controller(self, menu, mock_sample_ctrl, mock_view):
        mock_view.show_menu.side_effect = ["1", "7"]
        menu.run()
        mock_sample_ctrl.run.assert_called_once()

    def test_choice_2_runs_order_controller(self, menu, mock_order_ctrl, mock_view):
        mock_view.show_menu.side_effect = ["2", "7"]
        menu.run()
        mock_order_ctrl.run.assert_called_once()

    def test_choice_3_runs_monitoring_controller(self, menu, mock_monitoring_ctrl, mock_view):
        mock_view.show_menu.side_effect = ["3", "7"]
        menu.run()
        mock_monitoring_ctrl.run.assert_called_once()

    def test_choice_4_runs_production_controller(self, menu, mock_production_ctrl, mock_view):
        mock_view.show_menu.side_effect = ["4", "7"]
        menu.run()
        mock_production_ctrl.run.assert_called_once()

    def test_choice_5_runs_release_controller(self, menu, mock_release_ctrl, mock_view):
        mock_view.show_menu.side_effect = ["5", "7"]
        menu.run()
        mock_release_ctrl.run.assert_called_once()

    def test_choice_6_resets_data_when_confirmed(self, menu, mock_reset_svc, mock_view):
        mock_view.show_menu.side_effect = ["6", "7"]
        mock_view.confirm_reset.return_value = True
        menu.run()
        mock_reset_svc.reset.assert_called_once()

    def test_choice_6_skips_reset_when_not_confirmed(self, menu, mock_reset_svc, mock_view):
        mock_view.show_menu.side_effect = ["6", "7"]
        mock_view.confirm_reset.return_value = False
        menu.run()
        mock_reset_svc.reset.assert_not_called()

    def test_choice_7_exits(self, menu, mock_view):
        mock_view.show_menu.return_value = "7"
        menu.run()
        mock_view.show_menu.assert_called_once()

    def test_invalid_choice_shows_error(self, menu, mock_view):
        mock_view.show_menu.side_effect = ["9", "7"]
        menu.run()
        mock_view.show_error.assert_called_once()

    def test_summary_is_shown_each_iteration(self, menu, mock_view, mock_monitoring_ctrl):
        mock_monitoring_ctrl._service.get_summary.return_value = {
            "sample_count": 2, "reserved": 1, "producing": 0, "confirmed": 0, "released": 3
        }
        mock_view.show_menu.return_value = "7"
        menu.run()
        mock_view.show_summary.assert_called_once()
        call_args = mock_view.show_summary.call_args[0][0]
        assert call_args["sample_count"] == 2

    def test_summary_returns_empty_dict_on_exception(self, menu, mock_view, mock_monitoring_ctrl):
        mock_monitoring_ctrl._service.get_summary.side_effect = Exception("db error")
        mock_view.show_menu.return_value = "7"
        menu.run()
        call_args = mock_view.show_summary.call_args[0][0]
        assert call_args == {}
