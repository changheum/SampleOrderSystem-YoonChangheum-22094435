import pytest
from src.production_calculator import ProductionCalculator, DEFAULT_SAFETY_FACTOR


@pytest.fixture
def calc():
    return ProductionCalculator()


class TestProductionCalculatorQuantity:
    def test_calculates_quantity_with_ceil(self, calc):
        # shortage=10, yield_rate=0.9 → ceil(10 / (0.9*0.9)) = ceil(12.35) = 13
        assert calc.calculate_quantity(10, 0.9) == 13

    def test_calculates_quantity_with_perfect_yield(self, calc):
        # shortage=9, yield_rate=1.0 → ceil(9 / (1.0*0.9)) = ceil(10.0) = 10
        assert calc.calculate_quantity(9, 1.0) == 10

    def test_calculates_quantity_rounds_up(self, calc):
        # shortage=1, yield_rate=1.0 → ceil(1/0.9) = ceil(1.111) = 2
        assert calc.calculate_quantity(1, 1.0) == 2

    def test_calculates_quantity_for_large_shortage(self, calc):
        # shortage=100, yield_rate=0.5 → ceil(100/(0.5*0.9)) = ceil(222.22) = 223
        assert calc.calculate_quantity(100, 0.5) == 223

    def test_calculates_quantity_with_low_yield(self, calc):
        # shortage=9, yield_rate=0.9 → ceil(9/(0.9*0.9)) = ceil(11.11) = 12
        assert calc.calculate_quantity(9, 0.9) == 12

    def test_raises_when_shortage_is_zero(self, calc):
        with pytest.raises(ValueError, match="shortage"):
            calc.calculate_quantity(0, 0.9)

    def test_raises_when_shortage_is_negative(self, calc):
        with pytest.raises(ValueError, match="shortage"):
            calc.calculate_quantity(-1, 0.9)

    def test_raises_when_yield_rate_is_zero(self, calc):
        with pytest.raises(ValueError, match="yield_rate"):
            calc.calculate_quantity(10, 0.0)

    def test_raises_when_yield_rate_exceeds_one(self, calc):
        with pytest.raises(ValueError, match="yield_rate"):
            calc.calculate_quantity(10, 1.1)

    def test_custom_safety_factor_changes_result(self):
        strict_calc = ProductionCalculator(safety_factor=0.5)
        # shortage=10, yield_rate=1.0 → ceil(10/(1.0*0.5)) = 20
        assert strict_calc.calculate_quantity(10, 1.0) == 20

    def test_raises_when_safety_factor_is_zero(self):
        with pytest.raises(ValueError, match="safety_factor"):
            ProductionCalculator(safety_factor=0.0)

    def test_raises_when_safety_factor_exceeds_one(self):
        with pytest.raises(ValueError, match="safety_factor"):
            ProductionCalculator(safety_factor=1.1)

    def test_default_safety_factor_constant(self):
        assert DEFAULT_SAFETY_FACTOR == 0.9


class TestProductionCalculatorDuration:
    def test_calculates_duration(self, calc):
        assert calc.calculate_duration(60, 10) == 600

    def test_calculates_duration_single_unit(self, calc):
        assert calc.calculate_duration(120, 1) == 120

    def test_raises_when_avg_production_time_is_zero(self, calc):
        with pytest.raises(ValueError, match="avg_production_time"):
            calc.calculate_duration(0, 10)

    def test_raises_when_quantity_is_zero(self, calc):
        with pytest.raises(ValueError, match="quantity"):
            calc.calculate_duration(60, 0)
