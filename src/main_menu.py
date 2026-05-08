from src.controllers.sample_controller import SampleController
from src.controllers.order_controller import OrderController
from src.controllers.monitoring_controller import MonitoringController
from src.controllers.production_controller import ProductionController
from src.controllers.release_controller import ReleaseController
from src.views.main_view import MainView


class MainMenu:
    def __init__(
        self,
        sample_ctrl: SampleController,
        order_ctrl: OrderController,
        monitoring_ctrl: MonitoringController,
        production_ctrl: ProductionController,
        release_ctrl: ReleaseController,
        view: MainView = None,
    ):
        self._sample_ctrl = sample_ctrl
        self._order_ctrl = order_ctrl
        self._monitoring_ctrl = monitoring_ctrl
        self._production_ctrl = production_ctrl
        self._release_ctrl = release_ctrl
        self._view = view or MainView()
        self._menu_actions = {
            "1": self._sample_ctrl.run,
            "2": self._order_ctrl.run,
            "3": self._monitoring_ctrl.run,
            "4": self._production_ctrl.run,
            "5": self._release_ctrl.run,
        }

    def run(self) -> None:
        while True:
            summary = self._build_summary()
            self._view.show_summary(summary)
            choice = self._view.show_menu()
            if choice == "6":
                self._view.show_goodbye()
                break
            action = self._menu_actions.get(choice)
            if action:
                action()
            else:
                self._view.show_error("올바른 메뉴 번호를 선택하세요. (1~6)")

    def _build_summary(self) -> dict:
        try:
            orders_by_status = self._monitoring_ctrl._service.get_orders_by_status()
            sample_count = len(self._monitoring_ctrl._service._sample_repo.find_all())
            from src.models import OrderStatus
            return {
                "sample_count": sample_count,
                "reserved": len(orders_by_status.get(OrderStatus.RESERVED, [])),
                "producing": len(orders_by_status.get(OrderStatus.PRODUCING, [])),
                "confirmed": len(orders_by_status.get(OrderStatus.CONFIRMED, [])),
                "released": len(orders_by_status.get(OrderStatus.RELEASE, [])),
            }
        except Exception:
            return {}
