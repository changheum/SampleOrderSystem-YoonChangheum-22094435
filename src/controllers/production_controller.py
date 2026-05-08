from src.production_service import ProductionService
from src.views.base_view import AbstractProductionView
from src.views.production_view import ProductionView


class ProductionController:
    def __init__(self, service: ProductionService, view: AbstractProductionView = None):
        self._service = service
        self._view = view or ProductionView()

    def show_status(self) -> None:
        self._view.show_current_job(self._service.get_current_job_progress())
        self._view.show_waiting_jobs(self._service.get_waiting_jobs())

    def run(self) -> None:
        while True:
            choice = self._view.show_menu()
            if choice == "1":
                self._service.restore()
                self.show_status()
            elif choice == "2":
                break
            else:
                self._view.show_error("올바른 메뉴 번호를 선택하세요. (1~2)")
