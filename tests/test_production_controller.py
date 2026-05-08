import pytest
from unittest.mock import MagicMock, patch
from src.models import Order, OrderStatus
from src.production_queue import ProductionJob
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


@pytest.fixture
def sample_job():
    return ProductionJob(job_id="J001", order_id="O001", sample_id="S001", target_quantity=13, total_duration=780)


class TestProductionControllerShowStatus:
    def test_show_status_passes_waiting_jobs_to_view(self, controller, mock_service, mock_view, sample_job):
        mock_service.get_current_job_progress.return_value = None
        mock_service.get_waiting_jobs.return_value = [sample_job]
        controller.show_status()
        mock_view.show_waiting_jobs.assert_called_once_with([sample_job])




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

    def test_show_status_calls_restore_before_showing(self, controller, mock_service, mock_view):
        mock_service.restore.return_value = []
        mock_service.get_current_job_progress.return_value = None
        mock_service.get_waiting_jobs.return_value = []
        controller.show_status()
        mock_service.restore.assert_called_once()

    def test_show_status_restore_called_before_get_progress(self, controller, mock_service, mock_view):
        call_order = []
        mock_service.restore.side_effect = lambda: call_order.append("restore") or []
        mock_service.get_current_job_progress.side_effect = lambda: call_order.append("progress") or None
        mock_service.get_waiting_jobs.return_value = []
        controller.show_status()
        assert call_order == ["restore", "progress"]


class TestProductionControllerCompleteJobWithList:
    def test_complete_job_shows_job_list_with_current_and_waiting(self, controller, mock_service, mock_view, sample_job):
        waiting = ProductionJob(job_id="J002", order_id="O002", sample_id="S001", target_quantity=5, total_duration=300)
        mock_service.get_current_job.return_value = sample_job
        mock_service.get_waiting_jobs.return_value = [waiting]
        mock_view.show_jobs_for_selection.return_value = None
        controller.complete_job()
        mock_view.show_jobs_for_selection.assert_called_once_with([sample_job, waiting])

    def test_complete_job_calls_service_with_selected_job_id(self, controller, mock_service, mock_view, sample_job):
        mock_service.get_current_job.return_value = sample_job
        mock_service.get_waiting_jobs.return_value = []
        mock_view.show_jobs_for_selection.return_value = sample_job
        mock_service.complete_job.return_value = Order(
            order_id="O001", sample_id="S001", customer_name="Lab", quantity=10, status=OrderStatus.CONFIRMED
        )
        controller.complete_job()
        mock_service.complete_job.assert_called_once_with("J001")

    def test_complete_job_shows_success_after_list_selection(self, controller, mock_service, mock_view, sample_job):
        mock_service.get_current_job.return_value = sample_job
        mock_service.get_waiting_jobs.return_value = []
        mock_view.show_jobs_for_selection.return_value = sample_job
        mock_service.complete_job.return_value = Order(
            order_id="O001", sample_id="S001", customer_name="Lab", quantity=10, status=OrderStatus.CONFIRMED
        )
        controller.complete_job()
        mock_view.show_complete_success.assert_called_once_with("O001")

    def test_complete_job_skips_when_no_selection(self, controller, mock_service, mock_view, sample_job):
        mock_service.get_current_job.return_value = sample_job
        mock_service.get_waiting_jobs.return_value = []
        mock_view.show_jobs_for_selection.return_value = None
        controller.complete_job()
        mock_service.complete_job.assert_not_called()

    def test_complete_job_shows_error_on_service_failure(self, controller, mock_service, mock_view, sample_job):
        mock_service.get_current_job.return_value = sample_job
        mock_service.get_waiting_jobs.return_value = []
        mock_view.show_jobs_for_selection.return_value = sample_job
        mock_service.complete_job.side_effect = ValueError("Job not found")
        controller.complete_job()
        mock_view.show_error.assert_called_once()


class TestProductionControllerRun:
    def test_run_show_status_then_exit(self, controller, mock_service, mock_view):
        mock_view.show_menu.side_effect = ["1", "3"]
        mock_service.get_current_job_progress.return_value = None
        mock_service.get_waiting_jobs.return_value = []
        controller.run()
        mock_service.get_current_job_progress.assert_called_once()

    def test_run_complete_then_exit(self, controller, mock_service, mock_view):
        mock_view.show_menu.side_effect = ["2", "3"]
        mock_service.get_current_job.return_value = None
        mock_service.get_waiting_jobs.return_value = []
        mock_view.show_jobs_for_selection.return_value = None
        controller.run()

    def test_run_invalid_choice_shows_error(self, controller, mock_service, mock_view):
        mock_view.show_menu.side_effect = ["9", "3"]
        controller.run()
        mock_view.show_error.assert_called_once()
