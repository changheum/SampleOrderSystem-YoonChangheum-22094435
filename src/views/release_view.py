from src.models import Order


class ReleaseView:
    def show_confirmed_list_and_select(self, orders: list[Order]) -> str:
        print("\n=== 출고 대기 주문 목록 ===")
        print(f"{'주문 ID':<38} {'시료 ID':<10} {'고객명':<20} {'수량'}")
        print("-" * 80)
        for o in orders:
            print(f"{o.order_id:<38} {o.sample_id:<10} {o.customer_name:<20} {o.quantity}")
        return input("\n출고할 주문 ID를 입력하세요: ").strip()

    def show_release_success(self, order_id: str) -> None:
        print(f"[완료] 주문 {order_id} 출고 처리 완료 → RELEASE")

    def show_error(self, message: str) -> None:
        print(f"[오류] {message}")

    def show_menu(self) -> str:
        print("\n=== 출고 처리 ===")
        print("1. 출고 실행")
        print("2. 뒤로가기")
        return input("선택: ").strip()
