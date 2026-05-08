import pytest
from unittest.mock import MagicMock, patch
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
def mock_view():
    return MagicMock()


@pytest.fixture
def menu(mock_sample_ctrl, mock_order_ctrl, mock_monitoring_ctrl, mock_production_ctrl, mock_release_ctrl, mock_view):
    return MainMenu(
        sample_ctrl=mock_sample_ctrl,
        order_ctrl=mock_order_ctrl,
        monitoring_ctrl=mock_monitoring_ctrl,
        production_ctrl=mock_production_ctrl,
        release_ctrl=mock_release_ctrl,
        view=mock_view,
    )


class TestMainMenuRun:
    def test_choice_1_runs_sample_controller(self, menu, mock_sample_ctrl, mock_view):
        mock_view.show_menu.side_effect = ["1", "6"]
        menu.run()
        mock_sample_ctrl.run.assert_called_once()

    def test_choice_2_runs_order_controller(self, menu, mock_order_ctrl, mock_view):
        mock_view.show_menu.side_effect = ["2", "6"]
        menu.run()
        mock_order_ctrl.run.assert_called_once()

    def test_choice_3_runs_monitoring_controller(self, menu, mock_monitoring_ctrl, mock_view):
        mock_view.show_menu.side_effect = ["3", "6"]
        menu.run()
        mock_monitoring_ctrl.run.assert_called_once()

    def test_choice_4_runs_production_controller(self, menu, mock_production_ctrl, mock_view):
        mock_view.show_menu.side_effect = ["4", "6"]
        menu.run()
        mock_production_ctrl.run.assert_called_once()

    def test_choice_5_runs_release_controller(self, menu, mock_release_ctrl, mock_view):
        mock_view.show_menu.side_effect = ["5", "6"]
        menu.run()
        mock_release_ctrl.run.assert_called_once()

    def test_choice_6_exits(self, menu, mock_view):
        mock_view.show_menu.return_value = "6"
        menu.run()
        mock_view.show_menu.assert_called_once()

    def test_invalid_choice_shows_error(self, menu, mock_view):
        mock_view.show_menu.side_effect = ["9", "6"]
        menu.run()
        mock_view.show_error.assert_called_once()

    def test_summary_is_shown_each_iteration(self, menu, mock_view, mock_monitoring_ctrl):
        mock_view.show_menu.side_effect = ["6"]
        mock_monitoring_ctrl.service = MagicMock()
        menu.run()
        mock_view.show_summary.assert_called_once()
