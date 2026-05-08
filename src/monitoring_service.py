from src.models import OrderStatus
from src.repository import OrderRepository, SampleRepository, InventoryRepository

_MONITORED_STATUSES = [
    OrderStatus.RESERVED,
    OrderStatus.PRODUCING,
    OrderStatus.CONFIRMED,
    OrderStatus.RELEASE,
]


class InventoryStatusLabel:
    SURPLUS = "여유"
    SHORTAGE = "부족"
    DEPLETED = "고갈"


class MonitoringService:
    def __init__(
        self,
        order_repo: OrderRepository,
        sample_repo: SampleRepository,
        inventory_repo: InventoryRepository,
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
            "status": self._label(stock, demand),
        }

    @staticmethod
    def _label(stock: int, demand: int) -> str:
        if stock == 0:
            return InventoryStatusLabel.DEPLETED
        if stock < demand:
            return InventoryStatusLabel.SHORTAGE
        return InventoryStatusLabel.SURPLUS
