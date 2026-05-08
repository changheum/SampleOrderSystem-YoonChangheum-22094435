# SampleOrderSystem

반도체 시료(Sample) 생산주문관리 시스템 — 가상의 반도체 회사 **S-Semi**를 위한 콘솔 기반 MVC 애플리케이션.

---

## 개요

S-Semi는 다양한 반도체 시료를 연구소·팹리스·대학 연구실에 납품합니다. 기존 엑셀/메모장 기반 관리의 한계를 극복하고자 주문 접수부터 생산, 출고까지 전 과정을 통합 관리하는 시스템입니다.

---

## 기능

| 메뉴 | 설명 |
|------|------|
| 시료 관리 | 시료 등록 / 조회 / 이름 검색 |
| 주문 | 주문 접수 (RESERVED) / 승인 / 거절 |
| 모니터링 | 상태별 주문 현황, 시료별 재고 상태 (여유/부족/고갈) |
| 생산 라인 | 현재 생산 현황 조회 (현재 생산량·완료 예정 시각 포함), 경과 시간 초과 시 자동 완료 |
| 출고 처리 | CONFIRMED 주문 출고 (→ RELEASE) |
| 데이터 초기화 | 전체 데이터 파일 초기화 |

### 주문 상태 흐름

```
RESERVED ──[승인]──▶ 재고 충분 ──▶ CONFIRMED ──[출고]──▶ RELEASE
                 └──▶ 재고 부족 ──▶ PRODUCING ──[생산완료]──▶ CONFIRMED
         ──[거절]──▶ REJECTED
```

### 생산 공식

- **실 생산량**: `ceil(부족분 / (수율 × 0.9))`
- **총 생산 시간**: `평균 생산시간 × 실 생산량`
- **현재 생산량 추정**: `floor(목표 생산량 × 경과 시간 / 총 생산 시간)`
- **스케줄링**: FIFO

---

## 기술 스택

- **언어**: Python 3.10
- **아키텍처**: Console MVC (Model-View-Controller)
- **테스트**: pytest, pytest-cov, pytest-timeout
- **영속성**: JSON 파일 기반

---

## 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 실행
python main.py
```

---

## 테스트

```bash
# 전체 테스트 + 커버리지
pytest --cov=src --cov-report=term-missing

# 단일 파일
pytest tests/test_models.py -v
```

**현재 상태**: 277 tests passed · 커버리지 99%

---

## 프로젝트 구조

```
SampleOrderSystem/
├── main.py                        # 진입점
├── src/
│   ├── models.py                  # Sample, Order, Inventory 도메인 모델
│   ├── production_queue.py        # AbstractProductionQueue, ProductionJob (FIFO)
│   ├── json_production_queue.py   # JSON 영속 큐 구현체
│   ├── production_service.py      # 생산 서비스 + ProgressCalculator
│   ├── order_service.py           # 주문 승인/거절/재고 처리
│   ├── sample_service.py          # 시료 관리
│   ├── monitoring_service.py      # 모니터링 집계
│   ├── release_service.py         # 출고 처리
│   ├── json_repository.py         # JSON 기반 Repository 구현체
│   ├── main_menu.py               # 메인 메뉴 라우터
│   ├── controllers/               # 각 메뉴별 Controller
│   └── views/                     # 각 메뉴별 View + ABC
├── tests/                         # pytest 테스트 (src 구조 미러링)
├── agents/                        # Claude Code 커스텀 에이전트 정의
├── PRD.md                         # 제품 요구사항 문서
└── Phase{1-10}.md                 # TDD Phase별 계획 문서
```

---

## 개발 방법론

모든 기능은 **TDD (Red → Green → Refactor)** 사이클로 개발됩니다.

1. **RED**: 실패하는 테스트 작성 후 커밋
2. **GREEN**: 최소 구현으로 테스트 통과 후 커밋
3. **REVIEW**: `code-quality-validator` 에이전트로 SOLID/OCP 검증 후 리팩터 커밋
4. 사용자 승인 → `git push`

### 사용 에이전트

| 에이전트 | 사용 시점 |
|----------|-----------|
| `tdd-ocp-implementer` | 새 기능 전체 TDD 사이클 |
| `code-quality-validator` | GREEN 완료 후 품질 검증 |
| `prd-compliance-reviewer` | 구현 완료 후 PRD 대응 검토 |
| `planning-consistency-validator` | Phase 계획 문서 일관성 검사 |

---

## Phase 진행 현황

| Phase | 내용 | 상태 |
|-------|------|------|
| 1 | 프로젝트 기반 + 도메인 모델 | ✅ |
| 2 | JSON Repository 영속성 | ✅ |
| 3 | 시료 관리 메뉴 (MVC) | ✅ |
| 4 | 주문 접수/승인/거절 | ✅ |
| 5 | 생산 라인 (FIFO Queue) | ✅ |
| 6 | 모니터링 | ✅ |
| 7 | 출고 처리 | ✅ |
| 8 | 메인 메뉴 통합 | ✅ |
| 9 | 생산 큐 영속성 및 재시작 복원 | ✅ |
| 10 | 생산 현황 — 진행량 및 완료 예정 시각 | ✅ |

---

## 개발자

- **윤창흠** (22094435)
