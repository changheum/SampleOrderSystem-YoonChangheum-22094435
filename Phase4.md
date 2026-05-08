# Phase 4: 주문 접수 / 승인 / 거절

## 목표

주문 접수(RESERVED), 승인(재고 확인 → CONFIRMED 또는 PRODUCING), 거절(REJECTED) 처리 구현.

## 작업 목록

### Service (`src/order_service.py`)
- [ ] `OrderService.place_order(sample_id, customer_name, quantity) -> Order` — RESERVED 상태로 등록
  - 존재하지 않는 sample_id 처리
- [ ] `OrderService.approve(order_id) -> Order` — 재고 확인 후 분기
  - 재고 충분 → Inventory 차감 + CONFIRMED
  - 재고 부족 → 부족분 생산 라인 등록 + PRODUCING
- [ ] `OrderService.reject(order_id) -> Order` — REJECTED 전환
- [ ] `OrderService.find_reserved() -> list[Order]` — RESERVED 목록 조회
- [ ] RESERVED 상태가 아닌 주문에 승인/거절 시도 방지

### View (`src/views/order_view.py`)
- [ ] 주문 접수 입력 화면
- [ ] RESERVED 목록 출력
- [ ] 승인/거절 선택 화면

### Controller (`src/controllers/order_controller.py`)
- [ ] 접수 / 승인 / 거절 흐름 연결

### 테스트 (`tests/test_order_service.py`, `tests/test_order_controller.py`)
- [ ] 정상 주문 접수 (RESERVED)
- [ ] 존재하지 않는 sample_id로 접수 시도
- [ ] 승인 — 재고 충분 케이스 (CONFIRMED, Inventory 차감 확인)
- [ ] 승인 — 재고 부족 케이스 (PRODUCING, 생산 라인 등록 확인)
- [ ] 승인 — 재고 정확히 0인 경계 케이스
- [ ] 거절 — REJECTED 전환
- [ ] RESERVED 아닌 주문 승인/거절 시도 → 예외

## TDD 단계

| 단계 | 내용 | 커밋 |
|------|------|------|
| RED | 실패하는 테스트 작성 | `[RED] Phase4 - order approval tests` |
| GREEN | 최소 구현으로 테스트 통과 | `[GREEN] Phase4 - order approval implementation` |
| REVIEW | code-quality-validator + OCP(재고 전략 분리 가능성) 체크 | `[REFACTOR] Phase4 - clean up order service` |

## 완료 기준

- `pytest --cov=src --cov-report=term-missing` → **~100%**
- 재고 확인 → 상태 전환 로직의 원자성 보장
- 사용자 승인 후 `git push`

## 상태

- [x] RED
- [x] GREEN
- [x] REVIEW
- [x] 승인 완료
- [x] git push 완료
