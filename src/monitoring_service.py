from enum import Enum
from src.models import OrderStatus
from src.protocols import ReadableOrderRepository, ReadableSampleRepository, ReadableInventoryRepository

_MONITORED_STATUSES = [
    OrderStatus.RESERVED,
    OrderStatus.PRODUCING,
    OrderStatus.CONFIRMED,
    OrderStatus.RELEASE,
]


class InventoryStatusLabel(str, Enum):
    SURPLUS  = "여유"
    SHORTAGE = "부족"
    DEPLETED = "고갈"

    @staticmethod
    def classify(stock: int, demand: int) -> "InventoryStatusLabel":
        if stock == 0:
            return InventoryStatusLabel.DEPLETED
        if stock < demand:
            return InventoryStatusLabel.SHORTAGE
        return InventoryStatusLabel.SURPLUS


class MonitoringService:
    def __init__(
        self,
        order_repo: ReadableOrderRepository,
        sample_repo: ReadableSampleRepository,
        inventory_repo: ReadableInventoryRepository,
    ):
        self._order_repo = order_repo
        self._sample_repo = sample_repo
        self._inventory_repo = inventory_repo

    def get_orders_by_status(self) -> dict:
        result = {status: [] for status in _MONITORED_STATUSES}
        for order in self._order_repo.find_all():
            if order.status in result:
                result[order.status].append(order)
        return result

    def get_summary(self) -> dict:
        orders_by_status = self.get_orders_by_status()
        sample_count = len(self._sample_repo.find_all())
        return {
            "sample_count": sample_count,
            "reserved": len(orders_by_status.get(OrderStatus.RESERVED, [])),
            "producing": len(orders_by_status.get(OrderStatus.PRODUCING, [])),
            "confirmed": len(orders_by_status.get(OrderStatus.CONFIRMED, [])),
            "released": len(orders_by_status.get(OrderStatus.RELEASE, [])),
        }

    def get_inventory_status(self) -> list[dict]:
        orders = [o for o in self._order_repo.find_all() if o.status != OrderStatus.REJECTED]
        return [self._build_status(sample, orders) for sample in self._sample_repo.find_all()]

    def _build_status(self, sample, orders) -> dict:
        demand = sum(o.quantity for o in orders if o.sample_id == sample.sample_id)
        inventory = self._inventory_repo.find_by_id(sample.sample_id)
        stock = inventory.stock_quantity if inventory else 0
        return {
            "sample": sample,
            "stock_quantity": stock,
            "status": InventoryStatusLabel.classify(stock, demand),
        }
