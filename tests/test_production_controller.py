import pytest
from unittest.mock import MagicMock
from src.controllers.production_controller import ProductionController


@pytest.fixture
def mock_service():
    return MagicMock()


@pytest.fixture
def mock_view():
    return MagicMock()


@pytest.fixture
def controller(mock_service, mock_view):
    return ProductionController(mock_service, mock_view)



class TestProductionControllerShowStatus:
    def test_show_status_passes_waiting_jobs_to_view(self, controller, mock_service, mock_view):
        mock_service.get_current_job_progress.return_value = None
        mock_service.get_waiting_jobs.return_value = ["job"]
        controller.show_status()
        mock_view.show_waiting_jobs.assert_called_once_with(["job"])




class TestProductionControllerShowStatusWithProgress:
    def test_show_status_calls_get_current_job_progress(self, controller, mock_service, mock_view):
        mock_service.get_current_job_progress.return_value = None
        mock_service.get_waiting_jobs.return_value = []
        controller.show_status()
        mock_service.get_current_job_progress.assert_called_once()

    def test_show_status_passes_progress_to_view(self, controller, mock_service, mock_view):
        mock_progress = MagicMock()
        mock_service.get_current_job_progress.return_value = mock_progress
        mock_service.get_waiting_jobs.return_value = []
        controller.show_status()
        mock_view.show_current_job.assert_called_once_with(mock_progress)


class TestProductionControllerRun:
    def test_run_show_status_then_exit(self, controller, mock_service, mock_view):
        mock_view.show_menu.side_effect = ["1", "2"]
        mock_service.restore.return_value = []
        mock_service.get_current_job_progress.return_value = None
        mock_service.get_waiting_jobs.return_value = []
        controller.run()
        mock_service.get_current_job_progress.assert_called_once()

    def test_run_calls_restore_before_show_status(self, controller, mock_service, mock_view):
        call_order = []
        mock_service.restore.side_effect = lambda: call_order.append("restore") or []
        mock_service.get_current_job_progress.side_effect = lambda: call_order.append("progress") or None
        mock_service.get_waiting_jobs.return_value = []
        mock_view.show_menu.side_effect = ["1", "2"]
        controller.run()
        assert call_order == ["restore", "progress"]

    def test_run_choice_2_exits(self, controller, mock_service, mock_view):
        mock_view.show_menu.return_value = "2"
        controller.run()
        mock_view.show_menu.assert_called_once()

    def test_run_invalid_choice_shows_error(self, controller, mock_service, mock_view):
        mock_view.show_menu.side_effect = ["9", "2"]
        controller.run()
        mock_view.show_error.assert_called_once()
