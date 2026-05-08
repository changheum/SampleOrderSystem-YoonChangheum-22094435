from src.monitoring_service import MonitoringService
from src.views.monitoring_view import MonitoringView


class MonitoringController:
    def __init__(self, service: MonitoringService, view: MonitoringView = None):
        self._service = service
        self._view = view or MonitoringView()

    def show_orders(self) -> None:
        data = self._service.get_orders_by_status()
        self._view.show_orders_by_status(data)

    def show_inventory(self) -> None:
        data = self._service.get_inventory_status()
        self._view.show_inventory_status(data)

    def run(self) -> None:
        while True:
            choice = self._view.show_menu()
            if choice == "1":
                self.show_orders()
            elif choice == "2":
                self.show_inventory()
            elif choice == "3":
                break
            else:
                self._view.show_error("올바른 메뉴 번호를 선택하세요. (1~3)")
