from abc import ABC, abstractmethod


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
