# Phase 10: 생산 현황 — 현재 생산량 및 완료 예정 시각 표시

## 목표

생산 현황 조회 화면에서 현재까지 생산된 물량(추정)과 생산 완료 예정 시각을 표시한다.

## 요구사항 (PRD)

- **현재 생산량**: `floor(목표 생산량 × 경과 시간 / 총 생산 시간)`, 목표 생산량 초과 불가
- **완료 예정 시각**: `started_at + total_duration`을 "YYYY-MM-DD HH:MM" 형식으로 표시
- `started_at` 미기록 시 현재 생산량 = 0, 완료 예정 시각 = "미정"

## 작업 목록

### 도메인 (`src/production_service.py`)
- [ ] `ProductionProgress` dataclass 추가 (`job`, `produced_quantity`, `estimated_completion`)
- [ ] `ProductionService.get_current_job_progress() -> ProductionProgress | None` 구현

### 뷰 / ABC (`src/views/`)
- [ ] `AbstractProductionView.show_current_job` 시그니처 변경: `ProductionJob | None` → `ProductionProgress | None`
- [ ] `ProductionView.show_current_job` 현재 생산량·완료 예정 시각 출력 추가

### 컨트롤러 (`src/controllers/production_controller.py`)
- [ ] `show_status()`: `get_current_job()` → `get_current_job_progress()` 호출

### 테스트
- [ ] `tests/test_production_service.py` — `get_current_job_progress()` 경과 시간별 시나리오
- [ ] `tests/test_production_view.py` — `show_current_job` 새 필드 출력 테스트
- [ ] `tests/test_production_controller.py` — `show_status` 업데이트 테스트

## TDD 단계

| 단계 | 내용 | 커밋 |
|------|------|------|
| RED | 실패 테스트 작성 | `[RED] Phase10 - 생산 현황 진행량 및 완료 시각 테스트` |
| GREEN | 최소 구현 | `[GREEN] Phase10 - 생산 현황 진행량 및 완료 시각 구현` |
| REVIEW | code-quality-validator + 리팩터 | `[REVIEW] Phase10 - ...` |

## 완료 기준

- `pytest --cov=src --cov-report=term-missing` → ~100%
- 사용자 승인 → git push

## 상태

- [ ] RED
- [ ] GREEN
- [ ] REVIEW
- [ ] 승인 완료
- [ ] git push 완료
