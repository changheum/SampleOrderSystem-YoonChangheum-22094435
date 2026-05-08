class MainView:
    def show_summary(self, summary: dict) -> None:
        print("\n" + "=" * 50)
        print("  S-Semi 반도체 시료 생산주문관리 시스템")
        print("=" * 50)
        print(f"  시료 수       : {summary.get('sample_count', 0)}종")
        print(f"  접수 대기     : {summary.get('reserved', 0)}건")
        print(f"  생산 중       : {summary.get('producing', 0)}건")
        print(f"  출고 대기     : {summary.get('confirmed', 0)}건")
        print(f"  출고 완료     : {summary.get('released', 0)}건")
        print("=" * 50)

    def show_menu(self) -> str:
        print("\n1. 시료 관리")
        print("2. 주문 (접수 / 승인 / 거절)")
        print("3. 모니터링")
        print("4. 생산 라인")
        print("5. 출고 처리")
        print("6. 종료")
        return input("선택: ").strip()

    def show_error(self, message: str) -> None:
        print(f"[오류] {message}")

    def show_goodbye(self) -> None:
        print("\n시스템을 종료합니다. 안녕히 가세요.")
