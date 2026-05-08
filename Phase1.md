# Phase 1: 프로젝트 기반 + 도메인 모델

## 목표

프로젝트 골격 구성 및 핵심 도메인 엔티티 정의. 이후 모든 Phase의 기반이 되는 계층.

## 작업 목록

### 프로젝트 기반
- [ ] `requirements.txt` — `pytest`, `pytest-cov`
- [ ] `src/__init__.py`, `tests/__init__.py`

### 도메인 모델 (`src/models.py`)
- [ ] `OrderStatus` — 상태 상수 (`RESERVED`, `REJECTED`, `PRODUCING`, `CONFIRMED`, `RELEASE`)
- [ ] `Sample` dataclass — `sample_id: str`, `name: str`, `avg_production_time: int` (>0), `yield_rate: float` (0 < y ≤ 1)
- [ ] `Order` dataclass — `order_id: str`, `sample_id: str`, `customer_name: str`, `quantity: int` (>0), `status: str`
- [ ] `Inventory` dataclass — `sample_id: str`, `stock_quantity: int` (≥0)
- [ ] 각 필드 유효성 검사 (`__post_init__`)

### 테스트 (`tests/test_models.py`)
- [ ] `Sample` 정상 생성
- [ ] `Sample` 유효성 실패 케이스 — `avg_production_time ≤ 0`, `yield_rate` 범위 초과
- [ ] `Order` 정상 생성
- [ ] `Order` 유효성 실패 케이스 — `quantity ≤ 0`, 유효하지 않은 `status`
- [ ] `Inventory` 정상 생성
- [ ] `Inventory` 유효성 실패 케이스 — `stock_quantity < 0`
- [ ] `OrderStatus` 상수값 검증

## TDD 단계

| 단계 | 내용 | 커밋 |
|------|------|------|
| RED | 실패하는 테스트 작성 | `[RED] Phase1 - domain model tests` |
| GREEN | 최소 구현으로 테스트 통과 | `[GREEN] Phase1 - domain model implementation` |
| REVIEW | code-quality-validator 실행 + SOLID 체크 + 리팩토링 | `[REFACTOR] Phase1 - clean up domain model` |

## 완료 기준

- `pytest --cov=src --cov-report=term-missing` → **100%**
- SOLID 원칙 위반 없음 (code-quality-validator 통과)
- 사용자 승인 후 `git push`

## 상태

- [x] RED
- [x] GREEN
- [x] REVIEW
- [ ] 승인 완료
- [ ] git push 완료
