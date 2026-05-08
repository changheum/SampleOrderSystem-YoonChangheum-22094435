from src.views.base_view import BaseSampleView
from src.views.shared import render_sample_table


class SampleView(BaseSampleView):
    def show_register_prompt(self) -> dict:
        print("\n=== 시료 등록 ===")
        return {
            "sample_id": input("시료 ID: ").strip(),
            "name": input("시료 이름: ").strip(),
            "avg_production_time": input("평균 생산시간 (분): ").strip(),
            "yield_rate": input("수율 (0 초과 ~ 1 이하): ").strip(),
        }

    def show_register_success(self, sample_id: str, name: str) -> None:
        print(f"[완료] 시료 등록 성공 — ID: {sample_id}, 이름: {name}")

    def show_error(self, message: str) -> None:
        print(f"[오류] {message}")

    def show_sample_list(self, entries: list[dict]) -> None:
        print("\n=== 시료 목록 ===")
        if not entries:
            print("등록된 시료가 없습니다.")
            return
        render_sample_table(entries)

    def show_search_prompt(self) -> str:
        return input("\n검색할 이름을 입력하세요: ").strip()

    def show_search_results(self, entries: list[dict]) -> None:
        if not entries:
            print("검색 결과가 없습니다.")
            return
        self.show_sample_list(entries)

    def show_menu(self) -> str:
        print("\n=== 시료 관리 ===")
        print("1. 시료 등록")
        print("2. 시료 조회")
        print("3. 시료 검색")
        print("4. 뒤로가기")
        return input("선택: ").strip()
