from src.sample_service import SampleService
from src.views.sample_view import SampleView


class SampleController:
    def __init__(self, service: SampleService, view: SampleView = None):
        self._service = service
        self._view = view or SampleView()

    def register(self) -> None:
        prompt = self._view.show_register_prompt()
        try:
            sample = self._service.register(
                sample_id=prompt["sample_id"],
                name=prompt["name"],
                avg_production_time=int(prompt["avg_production_time"]),
                yield_rate=float(prompt["yield_rate"]),
            )
            self._view.show_register_success(sample.sample_id, sample.name)
        except ValueError as e:
            self._view.show_error(str(e))

    def list_samples(self) -> None:
        entries = self._service.find_all()
        self._view.show_sample_list(entries)

    def search(self) -> None:
        keyword = self._view.show_search_prompt()
        results = self._service.search_by_name(keyword)
        self._view.show_search_results(results)

    def run(self) -> None:
        while True:
            choice = self._view.show_menu()
            if choice == "1":
                self.register()
            elif choice == "2":
                self.list_samples()
            elif choice == "3":
                self.search()
            elif choice == "4":
                break
