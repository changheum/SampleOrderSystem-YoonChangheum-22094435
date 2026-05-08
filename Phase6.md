# Phase 6: 모니터링

## 목표

상태별 주문 현황 및 시료별 재고 현황을 한눈에 파악할 수 있는 모니터링 화면 구현.

## 작업 목록

### Service (`src/monitoring_service.py`)
- [ ] `MonitoringService.get_orders_by_status() -> dict[str, list[Order]]`
  - RESERVED / PRODUCING / CONFIRMED / RELEASE 포함
  - **REJECTED 제외**
- [ ] `MonitoringService.get_inventory_status() -> list[InventoryStatus]`
  - `InventoryStatus` — `sample`, `stock_quantity`, `status: str`
  - 여유: 주문 대비 재고 충분 / 부족: 주문 대비 재고 부족 / 고갈: stock_quantity == 0

### View (`src/views/monitoring_view.py`)
- [ ] 상태별 주문 목록 출력 (REJECTED 미표시)
- [ ] 재고 현황 출력 (여유/부족/고갈 상태 표기)

### Controller (`src/controllers/monitoring_controller.py`)
- [ ] 모니터링 메뉴 흐름 연결

### 테스트 (`tests/test_monitoring_service.py`, `tests/test_monitoring_controller.py`)
- [ ] REJECTED 주문이 결과에 포함되지 않음 검증
- [ ] 각 상태별 주문 수 정확성
- [ ] 재고 0 → 고갈 표기
- [ ] 주문 대비 부족 → 부족 표기
- [ ] 주문 대비 충분 → 여유 표기
- [ ] 주문 없는 경우 경계 케이스

## TDD 단계

| 단계 | 내용 | 커밋 |
|------|------|------|
| RED | 실패하는 테스트 작성 | `[RED] Phase6 - monitoring tests` |
| GREEN | 최소 구현으로 테스트 통과 | `[GREEN] Phase6 - monitoring implementation` |
| REVIEW | code-quality-validator + REJECTED 제외 로직 검증 | `[REFACTOR] Phase6 - clean up monitoring` |

## 완료 기준

- `pytest --cov=src --cov-report=term-missing` → **~100%**
- REJECTED 주문 미표시 테스트 필수 포함
- 사용자 승인 후 `git push`

## 상태

- [x] RED
- [x] GREEN
- [x] REVIEW
- [x] 승인 완료
- [x] git push 완료
