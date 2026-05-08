# Phase 5: 생산 라인

## 목표

FIFO 생산 큐 구현, 생산량/생산시간 계산, 생산 완료 시 PRODUCING → CONFIRMED 전환.

## 작업 목록

### 생산 계산 (`src/production_calculator.py`)
- [ ] `ProductionCalculator.calculate_quantity(shortage: int, yield_rate: float) -> int`
  - 공식: `ceil(shortage / (yield_rate * 0.9))`
- [ ] `ProductionCalculator.calculate_duration(avg_production_time: int, quantity: int) -> int`
  - 공식: `avg_production_time * quantity`

### Production Queue (`src/production_queue.py`)
- [ ] `ProductionQueue` — FIFO 큐 (enqueue / dequeue / peek / list)
- [ ] `ProductionJob` dataclass — `order_id`, `sample_id`, `target_quantity`, `produced_quantity`, `total_duration`

### Service (`src/production_service.py`)
- [ ] `ProductionService.enqueue(order: Order, sample: Sample) -> ProductionJob` — 생산 등록
- [ ] `ProductionService.get_current_job() -> ProductionJob | None` — 현재 생산 중 항목
- [ ] `ProductionService.get_queue() -> list[ProductionJob]` — 대기 목록
- [ ] `ProductionService.complete_job(job_id) -> Order` — 생산 완료 → CONFIRMED 전환

### View (`src/views/production_view.py`)
- [ ] 현재 생산 중 항목 출력 (주문 정보, 현재 생산량)
- [ ] 대기 큐 목록 출력

### 테스트 (`tests/test_production_calculator.py`, `tests/test_production_queue.py`, `tests/test_production_service.py`)
- [ ] `calculate_quantity` — 정상값, 수율 경계값, 소수점 올림 케이스
- [ ] 큐 enqueue / dequeue FIFO 순서 검증
- [ ] 빈 큐에서 dequeue 처리
- [ ] 생산 완료 → 주문 상태 CONFIRMED 전환
- [ ] 생산 완료 후 Inventory 업데이트 확인

## TDD 단계

| 단계 | 내용 | 커밋 |
|------|------|------|
| RED | 실패하는 테스트 작성 | `[RED] Phase5 - production line tests` |
| GREEN | 최소 구현으로 테스트 통과 | `[GREEN] Phase5 - production line implementation` |
| REVIEW | code-quality-validator + SRP(계산/큐/서비스 분리) 체크 | `[REFACTOR] Phase5 - clean up production line` |

## 완료 기준

- `pytest --cov=src --cov-report=term-missing` → **~100%**
- `ceil(부족분 / (yield_rate * 0.9))` 공식 단위 테스트 포함
- FIFO 순서 보장 테스트 포함
- 사용자 승인 후 `git push`

## 상태

- [x] RED
- [x] GREEN
- [x] REVIEW
- [x] 승인 완료
- [x] git push 완료
