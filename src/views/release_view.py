from src.models import Order

_COL_ORDER_ID  = 38
_COL_SAMPLE_ID = 10
_COL_CUSTOMER  = 20


class ReleaseView:
    def show_confirmed_list(self, orders: list[Order]) -> None:
        print("\n=== 출고 대기 주문 목록 ===")
        print(f"{'주문 ID':<{_COL_ORDER_ID}} {'시료 ID':<{_COL_SAMPLE_ID}} {'고객명':<{_COL_CUSTOMER}} {'수량'}")
        print("-" * 80)
        for o in orders:
            print(f"{o.order_id:<{_COL_ORDER_ID}} {o.sample_id:<{_COL_SAMPLE_ID}} {o.customer_name:<{_COL_CUSTOMER}} {o.quantity}")

    def select_order_id(self) -> str:
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
