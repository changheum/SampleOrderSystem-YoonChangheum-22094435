import pytest
from src.production_calculator import ProductionCalculator


class TestProductionCalculatorQuantity:
    def test_calculates_quantity_with_ceil(self):
        # shortage=10, yield_rate=0.9 → ceil(10 / (0.9*0.9)) = ceil(10/0.81) = ceil(12.35) = 13
        assert ProductionCalculator.calculate_quantity(10, 0.9) == 13

    def test_calculates_quantity_with_perfect_yield(self):
        # shortage=9, yield_rate=1.0 → ceil(9 / (1.0*0.9)) = ceil(9/0.9) = ceil(10.0) = 10
        assert ProductionCalculator.calculate_quantity(9, 1.0) == 10

    def test_calculates_quantity_rounds_up(self):
        # shortage=1, yield_rate=1.0 → ceil(1/0.9) = ceil(1.111) = 2
        assert ProductionCalculator.calculate_quantity(1, 1.0) == 2

    def test_calculates_quantity_for_large_shortage(self):
        # shortage=100, yield_rate=0.5 → ceil(100/(0.5*0.9)) = ceil(100/0.45) = ceil(222.22) = 223
        assert ProductionCalculator.calculate_quantity(100, 0.5) == 223

    def test_calculates_quantity_exactly_divisible(self):
        # shortage=9, yield_rate=0.9 → ceil(9/(0.9*0.9)) = ceil(9/0.81) = ceil(11.11) = 12
        assert ProductionCalculator.calculate_quantity(9, 0.9) == 12

    def test_raises_when_shortage_is_zero(self):
        with pytest.raises(ValueError, match="shortage"):
            ProductionCalculator.calculate_quantity(0, 0.9)

    def test_raises_when_shortage_is_negative(self):
        with pytest.raises(ValueError, match="shortage"):
            ProductionCalculator.calculate_quantity(-1, 0.9)

    def test_raises_when_yield_rate_is_zero(self):
        with pytest.raises(ValueError, match="yield_rate"):
            ProductionCalculator.calculate_quantity(10, 0.0)

    def test_raises_when_yield_rate_exceeds_one(self):
        with pytest.raises(ValueError, match="yield_rate"):
            ProductionCalculator.calculate_quantity(10, 1.1)


class TestProductionCalculatorDuration:
    def test_calculates_duration(self):
        # avg_production_time=60, quantity=10 → 600
        assert ProductionCalculator.calculate_duration(60, 10) == 600

    def test_calculates_duration_single_unit(self):
        assert ProductionCalculator.calculate_duration(120, 1) == 120

    def test_raises_when_avg_production_time_is_zero(self):
        with pytest.raises(ValueError, match="avg_production_time"):
            ProductionCalculator.calculate_duration(0, 10)

    def test_raises_when_quantity_is_zero(self):
        with pytest.raises(ValueError, match="quantity"):
            ProductionCalculator.calculate_duration(60, 0)
