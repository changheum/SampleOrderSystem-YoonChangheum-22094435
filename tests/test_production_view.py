import pytest
from unittest.mock import patch
from src.production_queue import ProductionJob
from src.production_service import ProductionProgress
from src.views.production_view import ProductionView


@pytest.fixture
def view():
    return ProductionView()


@pytest.fixture
def sample_job():
    return ProductionJob(job_id="J001", order_id="O001", sample_id="S001", target_quantity=13, total_duration=780)


class TestProductionView:
    def test_show_current_job_prints_job_info(self, view, sample_job, capsys):
        progress = ProductionProgress(job=sample_job, produced_quantity=0, estimated_completion="2026-05-08 14:30")
        view.show_current_job(progress)
        out = capsys.readouterr().out
        assert "O001" in out
        assert "13" in out

    def test_show_current_job_prints_empty_message_when_none(self, view, capsys):
        view.show_current_job(None)
        assert "없습니다" in capsys.readouterr().out

    def test_show_waiting_jobs_prints_jobs(self, view, sample_job, capsys):
        view.show_waiting_jobs([sample_job])
        out = capsys.readouterr().out
        assert "O001" in out

    def test_show_waiting_jobs_prints_empty_message(self, view, capsys):
        view.show_waiting_jobs([])
        assert "없습니다" in capsys.readouterr().out

    def test_show_complete_prompt_returns_input(self, view):
        with patch("builtins.input", return_value="J001"):
            assert view.show_complete_prompt() == "J001"

    def test_show_complete_success_prints_order_id(self, view, capsys):
        view.show_complete_success("O001")
        assert "O001" in capsys.readouterr().out

    def test_show_error_prints_message(self, view, capsys):
        view.show_error("오류")
        assert "오류" in capsys.readouterr().out

    def test_show_menu_returns_choice(self, view):
        with patch("builtins.input", return_value="1"):
            assert view.show_menu() == "1"


class TestProductionViewWithProgress:
    def test_show_current_job_prints_produced_quantity(self, view, sample_job, capsys):
        progress = ProductionProgress(job=sample_job, produced_quantity=6, estimated_completion="2026-05-08 14:30")
        view.show_current_job(progress)
        assert "6" in capsys.readouterr().out

    def test_show_current_job_prints_estimated_completion(self, view, sample_job, capsys):
        progress = ProductionProgress(job=sample_job, produced_quantity=6, estimated_completion="2026-05-08 14:30")
        view.show_current_job(progress)
        assert "2026-05-08 14:30" in capsys.readouterr().out

    def test_show_current_job_prints_job_info(self, view, sample_job, capsys):
        progress = ProductionProgress(job=sample_job, produced_quantity=0, estimated_completion="2026-05-08 14:30")
        view.show_current_job(progress)
        out = capsys.readouterr().out
        assert "O001" in out
        assert "13" in out

    def test_show_current_job_prints_none_message_when_none(self, view, capsys):
        view.show_current_job(None)
        assert "없습니다" in capsys.readouterr().out


class TestProductionViewJobSelection:
    def test_show_jobs_for_selection_prints_numbered_list(self, view, sample_job, capsys):
        with patch("builtins.input", return_value=""):
            view.show_jobs_for_selection([sample_job])
        out = capsys.readouterr().out
        assert "1" in out
        assert "O001" in out

    def test_show_jobs_for_selection_returns_none_when_no_jobs(self, view, capsys):
        result = view.show_jobs_for_selection([])
        assert result is None
        assert "없습니다" in capsys.readouterr().out

    def test_show_jobs_for_selection_returns_selected_job(self, view, sample_job):
        with patch("builtins.input", return_value="1"):
            result = view.show_jobs_for_selection([sample_job])
        assert result == sample_job

    def test_show_jobs_for_selection_returns_none_on_empty_input(self, view, sample_job):
        with patch("builtins.input", return_value=""):
            result = view.show_jobs_for_selection([sample_job])
        assert result is None

    def test_show_jobs_for_selection_returns_none_on_out_of_range_input(self, view, sample_job):
        with patch("builtins.input", return_value="99"):
            result = view.show_jobs_for_selection([sample_job])
        assert result is None

    def test_show_jobs_for_selection_returns_none_on_non_numeric_input(self, view, sample_job):
        with patch("builtins.input", return_value="abc"):
            result = view.show_jobs_for_selection([sample_job])
        assert result is None
