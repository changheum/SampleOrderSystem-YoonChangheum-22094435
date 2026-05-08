from src.models import Order, OrderStatus
from src.repository import OrderRepository


class ReleaseService:
    def __init__(self, order_repo: OrderRepository):
        self._order_repo = order_repo

    def get_confirmed_orders(self) -> list[Order]:
        return [o for o in self._order_repo.find_all() if o.status == OrderStatus.CONFIRMED]

    def release(self, order_id: str) -> Order:
        order = self._order_repo.find_by_id(order_id)
        if order is None:
            raise ValueError(f"Order '{order_id}' not found")
        if order.status != OrderStatus.CONFIRMED:
            raise ValueError(f"Order must be in CONFIRMED status (current: {order.status})")
        released = Order(
            order_id=order.order_id,
            sample_id=order.sample_id,
            customer_name=order.customer_name,
            quantity=order.quantity,
            status=OrderStatus.RELEASE,
        )
        self._order_repo.save(released)
        return released
