from src.production_queue import ProductionJob


class ProductionView:
    def show_current_job(self, job: ProductionJob | None) -> None:
        print("\n=== 현재 생산 중 ===")
        if job is None:
            print("현재 생산 중인 작업이 없습니다.")
            return
        print(f"  주문 ID      : {job.order_id}")
        print(f"  시료 ID      : {job.sample_id}")
        print(f"  목표 생산량  : {job.target_quantity}")
        print(f"  총 생산 시간 : {job.total_duration}분")

    def show_waiting_jobs(self, jobs: list[ProductionJob]) -> None:
        print("\n=== 생산 대기 목록 ===")
        if not jobs:
            print("대기 중인 작업이 없습니다.")
            return
        print(f"{'주문 ID':<38} {'시료 ID':<10} {'목표 수량':<10} {'총 시간(분)'}")
        print("-" * 70)
        for j in jobs:
            print(f"{j.order_id:<38} {j.sample_id:<10} {j.target_quantity:<10} {j.total_duration}")

    def show_jobs_for_selection(self, jobs: list[ProductionJob]) -> ProductionJob | None:
        print("\n=== 생산 완료 처리 ===")
        if not jobs:
            print("생산 중인 작업이 없습니다.")
            return None
        print(f"{'번호':<6} {'주문 ID':<38} {'시료 ID':<10} {'목표 수량':<10} {'총 시간(분)'}")
        print("-" * 75)
        for i, job in enumerate(jobs, 1):
            print(f"{i:<6} {job.order_id:<38} {job.sample_id:<10} {job.target_quantity:<10} {job.total_duration}")
        choice = input("\n완료 처리할 번호를 선택하세요 (없으면 Enter): ").strip()
        if not choice:
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(jobs):
                return jobs[idx]
            return None
        except ValueError:
            return None

    def show_complete_prompt(self) -> str:
        return input("\n완료 처리할 Job ID를 입력하세요 (없으면 Enter): ").strip()

    def show_complete_success(self, order_id: str) -> None:
        print(f"[완료] 생산 완료 처리 — 주문 {order_id} → CONFIRMED")

    def show_error(self, message: str) -> None:
        print(f"[오류] {message}")

    def show_menu(self) -> str:
        print("\n=== 생산 라인 ===")
        print("1. 생산 현황 조회")
        print("2. 생산 완료 처리")
        print("3. 뒤로가기")
        return input("선택: ").strip()
