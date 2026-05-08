from src.models import Order
from src.views.shared import render_sample_table


class OrderView:
    def show_sample_list_for_order(self, entries: list[dict]) -> None:
        print("\n=== 주문 가능 시료 목록 ===")
        render_sample_table(entries)

    def show_place_order_prompt(self) -> dict:
        print("\n=== 주문 접수 ===")
        return {
            "sample_id": input("시료 ID: ").strip(),
            "customer_name": input("고객명: ").strip(),
            "quantity": input("주문 수량: ").strip(),
        }

    def show_place_order_success(self, order_id: str, status: str) -> None:
        print(f"[완료] 주문 접수 완료 — 주문 ID: {order_id}, 상태: {status}")

    def show_reserved_list_and_select(self, orders: list[Order]) -> str:
        print("\n=== 접수된 주문 목록 ===")
        print(f"{'주문 ID':<38} {'시료 ID':<10} {'고객명':<20} {'수량'}")
        print("-" * 80)
        for o in orders:
            print(f"{o.order_id:<38} {o.sample_id:<10} {o.customer_name:<20} {o.quantity}")
        return input("\n처리할 주문 ID를 입력하세요: ").strip()

    def show_approve_or_reject_prompt(self) -> str:
        print("1. 승인")
        print("2. 거절")
        return input("선택: ").strip()

    def show_approve_success(self, order_id: str, status: str) -> None:
        print(f"[완료] 주문 {order_id} → {status}")

    def show_reject_success(self, order_id: str) -> None:
        print(f"[완료] 주문 {order_id} → REJECTED")

    def show_error(self, message: str) -> None:
        print(f"[오류] {message}")

    def show_menu(self) -> str:
        print("\n=== 주문 관리 ===")
        print("1. 주문 접수")
        print("2. 승인/거절")
        print("3. 뒤로가기")
        return input("선택: ").strip()
