# Phase 3: 시료 관리 메뉴

## 목표

시료(Sample) 등록 / 조회 / 검색 기능 구현. Console MVC 패턴 연결 (Controller + View).

## 작업 목록

### Service (`src/sample_service.py`)
- [ ] `SampleService.register(sample_id, name, avg_production_time, yield_rate) -> Sample`
- [ ] `SampleService.find_all() -> list[Sample]` (재고 수량 포함)
- [ ] `SampleService.search_by_name(keyword: str) -> list[Sample]`
- [ ] 중복 `sample_id` 등록 방지

### View (`src/views/sample_view.py`)
- [ ] 시료 등록 입력 화면 렌더링
- [ ] 시료 목록 출력 (재고 수량 포함)
- [ ] 검색 결과 출력
- [ ] 뒤로가기

### Controller (`src/controllers/sample_controller.py`)
- [ ] 메뉴 선택 → Service 호출 → View 렌더링 연결

### 테스트
- [ ] `tests/test_sample_service.py` — 등록, 조회, 검색, 중복 등록 방지
- [ ] `tests/test_sample_controller.py` — 사용자 입력 mock 후 흐름 검증

## TDD 단계

| 단계 | 내용 | 커밋 |
|------|------|------|
| RED | 실패하는 테스트 작성 | `[RED] Phase3 - sample management tests` |
| GREEN | 최소 구현으로 테스트 통과 | `[GREEN] Phase3 - sample management implementation` |
| REVIEW | code-quality-validator + SRP(Service/View/Controller 분리) 체크 | `[REFACTOR] Phase3 - clean up sample management` |

## 완료 기준

- `pytest --cov=src --cov-report=term-missing` → **~100%**
- SRP: Service / View / Controller 명확히 분리
- 사용자 승인 후 `git push`

## 상태

- [ ] RED
- [ ] GREEN
- [ ] REVIEW
- [ ] 승인 완료
- [ ] git push 완료
