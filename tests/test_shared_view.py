import pytest
from src.models import Sample
from src.views.shared import render_sample_table


@pytest.fixture
def sample_entries():
    return [
        {
            "sample": Sample(sample_id="S001", name="GaN Wafer", avg_production_time=60, yield_rate=0.9),
            "stock_quantity": 100,
        },
        {
            "sample": Sample(sample_id="S002", name="SiC Chip", avg_production_time=30, yield_rate=0.8),
            "stock_quantity": 0,
        },
    ]


class TestRenderSampleTable:
    def test_renders_all_entries(self, sample_entries, capsys):
        render_sample_table(sample_entries)
        out = capsys.readouterr().out
        assert "GaN Wafer" in out
        assert "SiC Chip" in out

    def test_renders_header_row(self, sample_entries, capsys):
        render_sample_table(sample_entries)
        out = capsys.readouterr().out
        assert "생산시간" in out
        assert "수율" in out

    def test_renders_stock_quantities(self, sample_entries, capsys):
        render_sample_table(sample_entries)
        out = capsys.readouterr().out
        assert "100" in out
        assert "0" in out
