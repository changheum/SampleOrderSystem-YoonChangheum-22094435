import pytest
from unittest.mock import patch
from src.production_queue import ProductionJob
from src.views.production_view import ProductionView


@pytest.fixture
def view():
    return ProductionView()


@pytest.fixture
def sample_job():
    return ProductionJob(job_id="J001", order_id="O001", sample_id="S001", target_quantity=13, total_duration=780)


class TestProductionView:
    def test_show_current_job_prints_job_info(self, view, sample_job, capsys):
        view.show_current_job(sample_job)
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
