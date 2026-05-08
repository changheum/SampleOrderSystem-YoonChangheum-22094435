import math


class ProductionCalculator:
    @staticmethod
    def calculate_quantity(shortage: int, yield_rate: float) -> int:
        if shortage <= 0:
            raise ValueError("shortage must be a positive integer")
        if not (0 < yield_rate <= 1):
            raise ValueError("yield_rate must be in range (0, 1]")
        return math.ceil(shortage / (yield_rate * 0.9))

    @staticmethod
    def calculate_duration(avg_production_time: int, quantity: int) -> int:
        if avg_production_time <= 0:
            raise ValueError("avg_production_time must be greater than 0")
        if quantity <= 0:
            raise ValueError("quantity must be greater than 0")
        return avg_production_time * quantity
