import pytest
from unittest.mock import patch
from src.views.main_view import MainView


@pytest.fixture
def view():
    return MainView()


class TestMainView:
    def test_show_summary_prints_counts(self, view, capsys):
        view.show_summary({"sample_count": 3, "reserved": 2, "producing": 1, "confirmed": 4, "released": 10})
        out = capsys.readouterr().out
        assert "3종" in out
        assert "2건" in out

    def test_show_summary_handles_empty_dict(self, view, capsys):
        view.show_summary({})
        out = capsys.readouterr().out
        assert "0종" in out

    def test_show_menu_returns_choice(self, view):
        with patch("builtins.input", return_value="3"):
            assert view.show_menu() == "3"

    def test_show_error_prints_message(self, view, capsys):
        view.show_error("잘못된 입력")
        assert "잘못된 입력" in capsys.readouterr().out

    def test_show_goodbye_prints_message(self, view, capsys):
        view.show_goodbye()
        assert "종료" in capsys.readouterr().out
