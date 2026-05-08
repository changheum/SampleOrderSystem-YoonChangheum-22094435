# Phase 2: 데이터 영속성 (Data Persistence)

## 목표

JSON 파일 기반 Repository 계층 구현. 각 엔티티(Sample, Order, Inventory)에 대한 CRUD 및 파일 저장/불러오기 처리.

## 작업 목록

### Repository 인터페이스 (`src/repository.py`)
- [ ] `Repository` 추상 클래스 — `save`, `find_by_id`, `find_all`, `delete` 인터페이스 정의

### JSON Repository 구현 (`src/json_repository.py`)
- [ ] `JsonSampleRepository` — Sample CRUD + JSON 파일 저장/불러오기
- [ ] `JsonOrderRepository` — Order CRUD + JSON 파일 저장/불러오기
- [ ] `JsonInventoryRepository` — Inventory CRUD + JSON 파일 저장/불러오기
- [ ] 파일 없을 시 신규 생성, 있을 시 기존 데이터 유지

### 테스트 (`tests/test_repository.py`)
- [ ] 신규 파일 생성 케이스
- [ ] 저장 후 불러오기 (데이터 정합성)
- [ ] `find_by_id` — 존재/미존재 케이스
- [ ] `find_all` — 빈 목록, 다수 항목
- [ ] `delete` — 존재/미존재 케이스
- [ ] 기존 파일에 누적 저장 케이스
- [ ] 잘못된 경로 처리

## TDD 단계

| 단계 | 내용 | 커밋 |
|------|------|------|
| RED | 실패하는 테스트 작성 | `[RED] Phase2 - repository tests` |
| GREEN | 최소 구현으로 테스트 통과 | `[GREEN] Phase2 - json repository implementation` |
| REVIEW | code-quality-validator + SOLID 체크 (DIP: 추상 Repository에 의존) | `[REFACTOR] Phase2 - clean up repository` |

## 완료 기준

- `pytest --cov=src --cov-report=term-missing` → **~100%**
- Repository 구현체가 추상 인터페이스에 의존 (DIP 준수)
- 사용자 승인 후 `git push`

## 상태

- [x] RED
- [x] GREEN
- [x] REVIEW
- [ ] 승인 완료
- [ ] git push 완료
