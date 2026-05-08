# Phase 8: 통합 + 메인 메뉴 + 더미 데이터 + 최종 점검

## 목표

전체 시스템 통합. 메인 메뉴 진입점 구성, DummyDataGenerator 연동, 커버리지 최종 점검.

## 작업 목록

### 메인 메뉴 (`src/main_menu.py`, `main.py`)
- [ ] 전체 시료 요약 정보 표시 (메인 화면)
- [ ] 메뉴 선택 → 각 Controller 분기
  1. 시료 관리
  2. 주문 (접수/승인/거절)
  3. 모니터링
  4. 생산 라인
  5. 출고 처리
  6. 종료
- [ ] `main.py` — CLI 진입점

### DummyDataGenerator 연동 (`src/dummy_loader.py`)
- [ ] `DummyDataGenerator` PoC 모듈 연동
- [ ] 테스트용 더미 데이터 생성 및 로딩
- [ ] 통합 테스트용 픽스처로 활용

### 통합 테스트 (`tests/test_integration.py`)
- [ ] 전체 주문 흐름 시나리오: 접수 → 승인(재고 충분) → 출고
- [ ] 전체 주문 흐름 시나리오: 접수 → 승인(재고 부족) → 생산 완료 → 출고
- [ ] 접수 → 거절 흐름
- [ ] 메인 메뉴 선택 흐름 (사용자 입력 mock)

### 최종 점검
- [ ] `pytest --cov=src --cov-report=term-missing` → **~100%**
- [ ] prd-compliance-reviewer 에이전트 실행 — PRD 요구사항 전체 충족 확인
- [ ] planning-consistency-validator 실행 — Phase 문서와 구현 정합성 확인
- [ ] 전체 커버리지 리포트 캡처

## TDD 단계

| 단계 | 내용 | 커밋 |
|------|------|------|
| RED | 통합 시나리오 테스트 작성 | `[RED] Phase8 - integration tests` |
| GREEN | 메인 메뉴 + 통합 구현 | `[GREEN] Phase8 - main menu and integration` |
| REVIEW | 전체 SOLID + PRD 정합성 최종 점검 | `[REFACTOR] Phase8 - final cleanup` |

## 완료 기준

- `pytest --cov=src --cov-report=term-missing` → **~100%**
- prd-compliance-reviewer 통과
- 전체 주문 FSM 시나리오 통합 테스트 포함
- 사용자 최종 승인 후 `git push`

## 상태

- [x] RED
- [x] GREEN
- [x] REVIEW
- [ ] 승인 완료
- [ ] git push 완료
