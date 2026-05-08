from src.order_service import OrderService
from src.views.order_view import OrderView


class OrderController:
    def __init__(self, service: OrderService, view: OrderView = None):
        self._service = service
        self._view = view or OrderView()

    def place_order(self) -> None:
        prompt = self._view.show_place_order_prompt()
        try:
            order = self._service.place_order(
                prompt["sample_id"],
                prompt["customer_name"],
                int(prompt["quantity"]),
            )
            self._view.show_place_order_success(order.order_id, order.status.value)
        except ValueError as e:
            self._view.show_error(str(e))

    def approve_or_reject(self) -> None:
        reserved = self._service.find_reserved()
        if not reserved:
            self._view.show_error("처리 가능한 접수 주문이 없습니다.")
            return
        order_id = self._view.show_reserved_list_and_select(reserved)
        choice = self._view.show_approve_or_reject_prompt()
        try:
            if choice == "1":
                order = self._service.approve(order_id)
                self._view.show_approve_success(order.order_id, order.status.value)
            elif choice == "2":
                order = self._service.reject(order_id)
                self._view.show_reject_success(order.order_id)
            else:
                self._view.show_error("승인(1) 또는 거절(2)을 선택하세요.")
        except ValueError as e:
            self._view.show_error(str(e))

    def run(self) -> None:
        while True:
            choice = self._view.show_menu()
            if choice == "1":
                self.place_order()
            elif choice == "2":
                self.approve_or_reject()
            elif choice == "3":
                break
            else:
                self._view.show_error("올바른 메뉴 번호를 선택하세요. (1~3)")
