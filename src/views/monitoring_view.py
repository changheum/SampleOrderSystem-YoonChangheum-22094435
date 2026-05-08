from src.models import OrderStatus


class MonitoringView:
    def show_orders_by_status(self, orders_by_status: dict) -> None:
        print("\n=== 주문 현황 모니터링 ===")
        for status, orders in orders_by_status.items():
            print(f"\n[{status.value}] — {len(orders)}건")
            if orders:
                print(f"  {'주문 ID':<38} {'시료 ID':<10} {'고객명':<20} {'수량'}")
                print("  " + "-" * 72)
                for o in orders:
                    print(f"  {o.order_id:<38} {o.sample_id:<10} {o.customer_name:<20} {o.quantity}")

    def show_inventory_status(self, entries: list[dict]) -> None:
        print("\n=== 재고 현황 모니터링 ===")
        if not entries:
            print("등록된 시료가 없습니다.")
            return
        print(f"{'시료 ID':<10} {'이름':<20} {'재고':<8} {'상태'}")
        print("-" * 44)
        for entry in entries:
            s = entry["sample"]
            print(f"{s.sample_id:<10} {s.name:<20} {entry['stock_quantity']:<8} {entry['status']}")

    def show_error(self, message: str) -> None:
        print(f"[오류] {message}")

    def show_menu(self) -> str:
        print("\n=== 모니터링 ===")
        print("1. 주문 현황")
        print("2. 재고 현황")
        print("3. 뒤로가기")
        return input("선택: ").strip()
