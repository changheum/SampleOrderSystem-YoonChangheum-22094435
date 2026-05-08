# Phase 7: 출고 처리

## 목표

CONFIRMED 상태 주문에 대해 출고 실행 → RELEASE 전환 및 출고 완료 정보 저장.

## 작업 목록

### Service (`src/release_service.py`)
- [ ] `ReleaseService.get_confirmed_orders() -> list[Order]` — 출고 대기 목록 조회
- [ ] `ReleaseService.release(order_id) -> Order` — CONFIRMED → RELEASE 전환 + 완료 정보 저장
  - CONFIRMED 아닌 주문에 출고 시도 시 예외
- [ ] 출고 완료 정보 영속성 저장

### View (`src/views/release_view.py`)
- [ ] CONFIRMED 주문 목록 출력
- [ ] 특정 주문 출고 실행 화면
- [ ] 출고 완료 확인 메시지

### Controller (`src/controllers/release_controller.py`)
- [ ] 출고 처리 메뉴 흐름 연결

### 테스트 (`tests/test_release_service.py`, `tests/test_release_controller.py`)
- [ ] CONFIRMED 주문 목록 조회
- [ ] 정상 출고 → RELEASE 전환
- [ ] 출고 완료 정보 저장 확인
- [ ] CONFIRMED 아닌 주문 출고 시도 → 예외
- [ ] 빈 CONFIRMED 목록 처리

## TDD 단계

| 단계 | 내용 | 커밋 |
|------|------|------|
| RED | 실패하는 테스트 작성 | `[RED] Phase7 - release tests` |
| GREEN | 최소 구현으로 테스트 통과 | `[GREEN] Phase7 - release implementation` |
| REVIEW | code-quality-validator + 상태 전환 원자성 체크 | `[REFACTOR] Phase7 - clean up release` |

## 완료 기준

- `pytest --cov=src --cov-report=term-missing` → **~100%**
- CONFIRMED 외 상태 출고 시도 예외 테스트 필수
- 사용자 승인 후 `git push`

## 상태

- [x] RED
- [x] GREEN
- [x] REVIEW
- [x] 승인 완료
- [x] git push 완료
