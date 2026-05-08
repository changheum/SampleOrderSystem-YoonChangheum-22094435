from src.production_queue import ProductionJob
from src.production_service import ProductionProgress
from src.views.base_view import AbstractProductionView


class ProductionView(AbstractProductionView):
    def show_current_job(self, progress: ProductionProgress | None) -> None:
        print("\n=== 현재 생산 중 ===")
        if progress is None:
            print("현재 생산 중인 작업이 없습니다.")
            return
        job = progress.job
        print(f"  주문 ID        : {job.order_id}")
        print(f"  시료 ID        : {job.sample_id}")
        print(f"  목표 생산량    : {job.target_quantity}")
        print(f"  현재 생산량    : {progress.produced_quantity}")
        print(f"  총 생산 시간   : {job.total_duration}분")
        print(f"  완료 예정 시각 : {progress.estimated_completion}")

    def show_waiting_jobs(self, jobs: list[ProductionJob]) -> None:
        print("\n=== 생산 대기 목록 ===")
        if not jobs:
            print("대기 중인 작업이 없습니다.")
            return
        print(f"{'주문 ID':<38} {'시료 ID':<10} {'목표 수량':<10} {'총 시간(분)'}")
        print("-" * 70)
        for j in jobs:
            print(f"{j.order_id:<38} {j.sample_id:<10} {j.target_quantity:<10} {j.total_duration}")

    def show_error(self, message: str) -> None:
        print(f"[오류] {message}")

    def show_menu(self) -> str:
        print("\n=== 생산 라인 ===")
        print("1. 생산 현황 조회")
        print("2. 뒤로가기")
        return input("선택: ").strip()
