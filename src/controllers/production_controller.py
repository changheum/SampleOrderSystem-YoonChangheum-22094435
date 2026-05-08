from src.production_service import ProductionService
from src.views.base_view import AbstractProductionView
from src.views.production_view import ProductionView


class ProductionController:
    def __init__(self, service: ProductionService, view: AbstractProductionView = None):
        self._service = service
        self._view = view or ProductionView()

    def show_status(self) -> None:
        self._view.show_current_job(self._service.get_current_job())
        self._view.show_waiting_jobs(self._service.get_waiting_jobs())

    def complete_job(self) -> None:
        all_jobs = []
        current = self._service.get_current_job()
        if current:
            all_jobs.append(current)
        all_jobs.extend(self._service.get_waiting_jobs())
        job = self._view.show_jobs_for_selection(all_jobs)
        if job is None:
            return
        try:
            order = self._service.complete_job(job.job_id)
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
