from abc import ABC, abstractmethod
from src.production_queue import ProductionJob
from src.production_service import ProductionProgress


class AbstractProductionView(ABC):
    @abstractmethod
    def show_current_job(self, progress: ProductionProgress | None) -> None: ...

    @abstractmethod
    def show_waiting_jobs(self, jobs: list[ProductionJob]) -> None: ...

    @abstractmethod
    def show_jobs_for_selection(self, jobs: list[ProductionJob]) -> ProductionJob | None: ...

    @abstractmethod
    def show_complete_success(self, order_id: str) -> None: ...

    @abstractmethod
    def show_error(self, message: str) -> None: ...

    @abstractmethod
    def show_menu(self) -> str: ...


class BaseSampleView(ABC):
    @abstractmethod
    def show_register_prompt(self) -> dict: ...

    @abstractmethod
    def show_register_success(self, sample_id: str, name: str) -> None: ...

    @abstractmethod
    def show_error(self, message: str) -> None: ...

    @abstractmethod
    def show_sample_list(self, entries: list[dict]) -> None: ...

    @abstractmethod
    def show_search_prompt(self) -> str: ...

    @abstractmethod
    def show_search_results(self, entries: list[dict]) -> None: ...

    @abstractmethod
    def show_menu(self) -> str: ...
