from src.release_service import ReleaseService
from src.views.release_view import ReleaseView


class ReleaseController:
    def __init__(self, service: ReleaseService, view: ReleaseView = None):
        self._service = service
        self._view = view or ReleaseView()

    def release(self) -> None:
        confirmed = self._service.get_confirmed_orders()
        if not confirmed:
            self._view.show_error("출고 가능한 주문이 없습니다.")
            return
        order_id = self._view.show_confirmed_list_and_select(confirmed)
        try:
            order = self._service.release(order_id)
            self._view.show_release_success(order.order_id)
        except ValueError as e:
            self._view.show_error(str(e))

    def run(self) -> None:
        while True:
            choice = self._view.show_menu()
            if choice == "1":
                self.release()
            elif choice == "2":
                break
            else:
                self._view.show_error("올바른 메뉴 번호를 선택하세요. (1~2)")
