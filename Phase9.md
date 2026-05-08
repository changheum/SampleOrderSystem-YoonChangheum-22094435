# Phase 9: 생산 큐 영속성 + 재시작 복원 + 데이터 초기화

## 목표

1. 생산 큐를 JSON 파일로 영속화하여 프로그램 재시작 후에도 복원
2. 재시작 시 경과 시간 계산 → 완료된 작업 자동 처리
3. 전체 데이터 초기화 기능 추가 (메인 메뉴)

## 작업 목록

### 도메인 변경 (`src/production_queue.py`)
- [ ] `ProductionJob`에 `started_at: str` (ISO 8601) 필드 추가
- [ ] `JsonProductionQueue` 클래스 구현 (`AbstractProductionQueue` 구현체)
  - `enqueue()` 시 `started_at = datetime.now().isoformat()` 기록 + JSON 저장
  - `complete()` 시 JSON에서 제거
  - `_load()` / `_save()` 내부 구현

### 복원 서비스 (`src/production_service.py`)
- [ ] `ProductionService.restore() -> list[Order]`
  - 큐의 각 Job을 순서대로 확인
  - `경과 시간 = now - started_at` (분 단위)
  - `경과 시간 >= total_duration` → 자동 완료 처리 (PRODUCING → CONFIRMED)
  - 완료 처리된 Order 목록 반환

### 데이터 초기화 (`src/data_reset_service.py`)
- [ ] `DataResetService.reset(data_dir: str) -> None`
  - data/ 디렉터리의 모든 JSON 파일 삭제 (samples, orders, inventories, queue)

### 메인 메뉴 변경
- [ ] 메뉴 항목 재구성
  - 1. 시료 관리
  - 2. 주문 (접수 / 승인 / 거절)
  - 3. 모니터링
  - 4. 생산 라인
  - 5. 출고 처리
  - 6. 데이터 초기화 (확인 후 실행)
  - 7. 종료
- [ ] `main.py` 시작 시 `ProductionService.restore()` 자동 호출

### 테스트
- [ ] `tests/test_json_production_queue.py` — enqueue/complete/persist/load
- [ ] `tests/test_production_restore.py` — 경과 시간별 자동 완료 시나리오
- [ ] `tests/test_data_reset_service.py` — 파일 삭제 동작

## TDD 단계

| 단계 | 내용 | 커밋 |
|------|------|------|
| RED | 실패하는 테스트 작성 | `[RED] Phase9 - queue persistence and restore tests` |
| GREEN | 최소 구현으로 테스트 통과 | `[GREEN] Phase9 - queue persistence and restore` |
| REVIEW | code-quality-validator + SOLID 체크 | `[REFACTOR] Phase9 - clean up` |

## 완료 기준

- `pytest --cov=src --cov-report=term-missing` → **~100%**
- 재시작 후 PRODUCING 주문 자동 복원 확인
- 경과 시간 초과 시 자동 CONFIRMED 처리 확인
- 사용자 승인 후 `git push`

## 상태

- [ ] RED
- [ ] GREEN
- [ ] REVIEW
- [ ] 승인 완료
- [ ] git push 완료
