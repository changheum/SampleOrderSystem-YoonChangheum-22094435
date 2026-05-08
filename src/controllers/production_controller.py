from src.production_service import ProductionService
from src.views.production_view import ProductionView


class ProductionController:
    def __init__(self, service: ProductionService, view: ProductionView = None):
        self._service = service
        self._view = view or ProductionView()

    def show_status(self) -> None:
        self._view.show_current_job(self._service.get_current_job())
        self._view.show_waiting_jobs(self._service.get_waiting_jobs())

    def complete_job(self) -> None:
        job_id = self._view.show_complete_prompt()
        if not job_id:
            return
        try:
            order = self._service.complete_job(job_id)
            self._view.show_complete_success(order.order_id)
        except ValueError as e:
            self._view.show_error(str(e))

    def run(self) -> None:
        while True:
            choice = self._view.show_menu()
            if choice == "1":
                self.show_status()
            elif choice == "2":
                self.complete_job()
            elif choice == "3":
                break
            else:
                self._view.show_error("올바른 메뉴 번호를 선택하세요. (1~3)")
