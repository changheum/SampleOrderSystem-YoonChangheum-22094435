import uuid
from src.models import Order, Inventory, OrderStatus
from src.repository import OrderRepository, SampleRepository, InventoryRepository


class OrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        sample_repo: SampleRepository,
        inventory_repo: InventoryRepository,
        production_queue,
    ):
        self._order_repo = order_repo
        self._sample_repo = sample_repo
        self._inventory_repo = inventory_repo
        self._production_queue = production_queue

    def place_order(self, sample_id: str, customer_name: str, quantity: int) -> Order:
        if self._sample_repo.find_by_id(sample_id) is None:
            raise ValueError(f"Sample '{sample_id}' not found")
        order = Order(
            order_id=str(uuid.uuid4()),
            sample_id=sample_id,
            customer_name=customer_name,
            quantity=quantity,
            status=OrderStatus.RESERVED,
        )
        self._order_repo.save(order)
        return order

    def approve(self, order_id: str) -> Order:
        order = self._get_reserved_order(order_id)
        sample = self._sample_repo.find_by_id(order.sample_id)
        inventory = self._inventory_repo.find_by_id(order.sample_id)
        stock = inventory.stock_quantity if inventory else 0

        if stock >= order.quantity:
            return self._confirm_with_stock(order, inventory, stock)
        return self._send_to_production(order, sample, stock)

    def reject(self, order_id: str) -> Order:
        order = self._get_reserved_order(order_id)
        updated = Order(
            order_id=order.order_id,
            sample_id=order.sample_id,
            customer_name=order.customer_name,
            quantity=order.quantity,
            status=OrderStatus.REJECTED,
        )
        self._order_repo.save(updated)
        return updated

    def find_reserved(self) -> list[Order]:
        return [o for o in self._order_repo.find_all() if o.status == OrderStatus.RESERVED]

    def _get_reserved_order(self, order_id: str) -> Order:
        order = self._order_repo.find_by_id(order_id)
        if order is None:
            raise ValueError(f"Order '{order_id}' not found")
        if order.status != OrderStatus.RESERVED:
            raise ValueError(f"Order must be in RESERVED status (current: {order.status})")
        return order

    def _confirm_with_stock(self, order: Order, inventory: Inventory, stock: int) -> Order:
        updated_inventory = Inventory(sample_id=order.sample_id, stock_quantity=stock - order.quantity)
        self._inventory_repo.save(updated_inventory)
        confirmed = Order(
            order_id=order.order_id,
            sample_id=order.sample_id,
            customer_name=order.customer_name,
            quantity=order.quantity,
            status=OrderStatus.CONFIRMED,
        )
        self._order_repo.save(confirmed)
        return confirmed

    def _send_to_production(self, order: Order, sample, stock: int) -> Order:
        producing = Order(
            order_id=order.order_id,
            sample_id=order.sample_id,
            customer_name=order.customer_name,
            quantity=order.quantity,
            status=OrderStatus.PRODUCING,
        )
        self._order_repo.save(producing)
        self._production_queue.enqueue(producing, sample)
        return producing
