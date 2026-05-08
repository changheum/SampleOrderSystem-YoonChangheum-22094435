# 배경

여기 가상의 반도체 회사 "S-Semi" 가 있습니다.
이 회사는 다양한 종류의 반도체 시료(Sample)를 생산하여 연구소, 팹리스(Fabless) 업체, 대학 연구실 등의 고객에게
납품하고 있습니다.
시료는 주문이 들어오면 웨이퍼 공정 설비를 통해 제작되고, 검수를 거쳐 고객에게 출고됩니다.
그런데 최근 들어 주문량이 급증하면서 문제가 생겼습니다.
"어, 이 주문 처리됐나요?"
"공정 예약을 했는데, 언제 완성되는지 모르겠어요."
"이미 충분한 시료 재고가 있는데, 왜 추가 공정이 돌아가고 있나요?"
엑셀과 메모장으로 주문을 관리하다 보니, 실수가 잦고 재고와 공정 현황을 한눈에 파악하기 어려웠습니다.
이러한 이유로 S-Semi에서는 더 체계적인 시료 관리를 위한 "반도체 시료 생산주문관리 시스템" 을 개발하기로 결정
했습니다.

# 흐름

시료에 대한 주문 등록을 하면 주문을 Reserved 상태로 등록함
Reserved에 대해 승인/거절을 입력 할 수 있음
거절 되면 주문을 Rejected 상태로 변경
주문이 승인 되면 재고 확인 과정을 거침
시료 재고확인 후, 주문에 대해 충분한 재고가 있으면 시료를 사용해서 주문을 출고하고 주문을  CONFIRMED(출고준비) 상태로 바꿈
출고준비상태의 주문을 RELEASED(출고 처리) 상태로 바꾸면 시료를 사용해서 주문을 출고시키고 정보를 완료 정보를 저장
재고확인 과정에서 재고가 부족하면 부족분량을 생산 요청하여 주문이 PRODUCING 상태가 됨.
부족분의 시료가 생산 완료가 되면 시료를 사용해서 주문을 CONFIRMED(출고준비) 상태로 바꿈(생산에 걸리는 시간은 수율과 생산시간을 고려해야한다)

# 모든 주문은 아래의 상태를 보유

REJECTED는 거절된 주문으로 정상 흐름 외의 상태이며 모니터링에서 제외

RESERVED / 주문 접수
REJECTED / 주문 거절
PRODUCING / 주문 승인 완료 및 재고 부족으로 생산 중
CONFIRMED / 주문 승인 완료 및 출고 대기 중
RELEASE / 출고 완료

# 용어 및 정의

## 시료

시료(Sample)는 이 시스템의 가장 기본이 되는 단위
각 시료는 고유한 이름과 속성을 가지며, 시스템에 등록된 시료만 주문 가능

# 메인 메뉴

전체 시료에 대한 요약 정보를 확인할 수 있게 한다.
기능(메뉴)별 선택 화면을 Display 해서 선택할 수 있게 한다.

## 메인 메뉴 항목과 의미

1. 시료 관리 : 새로운 시료 등록, 목록 조회, 이름 검색 기능
2. 주문 (접수 / 승인 / 거절) :  생산 라인 담당자의 승인·거절 처리
3. 모니터링 : 상태별 주문 수 및 시료별 재고 현황 확인
4. 생산 라인 : 현재 생산 중인 시료 및 대기 중인 생산 큐 확인
5. 출고 처리 : CONFIRMED 상태 주문에 대해 출고 실행
6. 종료

### 시료 관리 메뉴

1. 시료 등록 : 새로운 시료를 시스템에 추가(속성 값 : 시료 ID, 이름, 평균 생산시간, 수율)
2. 시료 조회 : 등록된 모든 시료 목록을 확인(현재 재고 수량도 함께 표시)
3. 시료 검색 : 이름 등 속성으로 특정 시료를 검색
4. 뒤로가기
* 수율이란? : (정상적인 시료 / 총 생산 시료)
ex) 100개 생산 중 정상적인 물품 90개 = 0.9

### 주문 (접수 / 승인 / 거절) 메뉴

1. 접수
고객이 시료를 요청하면 주문 담당자가 주문을 생성 가능
시료 예약
* 시료 목록을 보고 고객이 원하는 시료와 수량을 주문
* 접수되면 주문 상태는 RESERVED
예약시 입력 값
* 시료 ID
* 고객명
* 주문 수량
2. 승인/거절
접수된 주문(RESERVED) 목록을 확인. 특정 주문에 대하여 승인 혹은 거절 할 수 있는 화면
RESERVED 상태의 주문 목록 Display하여 확인 가능하게 함

a) 주문 승인
접수된 특정 주문에 대해 승인

* 승인시 재고 상황에 따라 2가지 방식으로 자동으로 처리
* 재고가 충분한 경우 → 시료를 사용하고, 주문을 즉시 CONFIRMED 상태로 전환
* 재고가 부족한 경우 → 모자란 시료 분량을 생산 라인에 자동으로 등록, 주문 상태를 PRODUCING으로 전환
b) 주문 거절
접수된 특정 주문에 대해 거절
즉시 REJECTED 상태로 전환

### 모니터링 메뉴

담당자가 현재 시스템의 상태를 한눈에 파악할 수 있도록 구성

주문량 확인

* 현재 상태별(RESERVED/CONFIRMED/ PRODUCING / RELEASE) 목록을 확인
* REJECTED 는 유효한 주문이 아니므로 보여주지 않음

재고량 확인
각 시료별 현재 재고 수량을 확인
주문대비 재고 수량에 따라 상태도 표기

* 여유 : 주문대비 재고 충분 상태
* 부족 : 주문대비 재고 수량 부족 상태
* 고갈 : 수량이 0인 상태

### 생산 라인 메뉴

생산라인에 대한 정보를 Display
주문량에 대한 부족분을 생산하되, 수율 및 오차를 고려하여 시료를 생산

* 실 생산량 : ceil(부족분 / (수율 \* 0.9))
* 총 생산 시간 : 평균 생산시간 \* 실 생산량
* 생산 완료시 주문상태 PRODUCING -> CONFIRMED 변경

생산 현황 표기

* 현재 생산중인 시료에 대한 정보 표기
ex) 주문 정보, 현재까지의 생산량 등
대기 주문 표기
생산라인의 대기열인 생산 큐를 이용
생산 작업을 대기하고 있는 목록을 출력
* 스케쥴링 전략 : FIFO

### 생산 큐 영속성 및 재시작 복원

생산 큐는 프로그램 종료 후에도 유지되어야 하며, 재시작 시 자동으로 복원되어야 한다.

**생산 시작 시각 기록**
* 각 생산 작업(Job)은 생산 시작 시각(`started_at`)을 기록한다.
* 생산 큐 전체를 JSON 파일로 영속화한다 (enqueue 시 저장, complete 시 삭제).

**재시작 복원 절차**
프로그램 시작 시 아래 절차를 자동으로 수행한다:
1. 저장된 생산 큐 JSON을 로드한다.
2. 각 Job에 대해 경과 시간을 계산한다: `경과 시간 = 현재 시각 - started_at`
3. `경과 시간 >= total_duration` 인 경우 → 생산 완료 자동 처리 (PRODUCING → CONFIRMED)
4. `경과 시간 < total_duration` 인 경우 → 큐에 복원 (남은 시간 유지)

**데이터 모델 변경**
* `ProductionJob`에 `started_at: str` (ISO 8601 형식) 필드 추가

### 출고 처리 메뉴

재고가 충분해진 CONFIRMED 주문에 대하여 출고를 처리할 수 있는 화면
특정 주문에 대해 출고를 실행
주문 상태가 RELEASE로 전환




모든 프로젝트 관련한 개발은 TDD 로 진행해야 하며, 적절한 상황에 Git push 가 될 수 있도록 구성

---

# DummyDataGenerator PoC — 개발 계획

## 모듈 목적

Test를 위한 Dummy Data를 생성하고, 생성된 데이터를 연결된 파일(JSON)에 추가(append)하는 도구.

## 데이터 모델 (생성 대상)

| 엔티티 | 필드 |
|--------|------|
| Sample (시료) | sample_id, name, avg_production_time(분), yield_rate(0~1) |
| Order (주문) | order_id, sample_id, customer_name, quantity, status |
| Inventory (재고) | sample_id, stock_quantity |

Order status 허용값: `RESERVED`, `REJECTED`, `PRODUCING`, `CONFIRMED`, `RELEASE`

실 생산량 공식: `ceil(부족분 / (yield_rate * 0.9))`

## Phase 계획

---

### Phase 1: 프로젝트 기반 설정 + 도메인 모델

**목표:** 프로젝트 구조 생성, 도메인 데이터 클래스(dataclass) 정의, 기본 유효성 검사

**작업 목록:**
- [x] `pytest`, `pytest-cov` 의존성 설정 (`requirements.txt`)
- [x] `src/models.py` — `Sample`, `Order`, `Inventory` dataclass 정의
  - Sample: sample_id(str), name(str), avg_production_time(int, >0), yield_rate(float, 0<y≤1)
  - Order: order_id(str), sample_id(str), customer_name(str), quantity(int, >0), status(str)
  - Inventory: sample_id(str), stock_quantity(int, ≥0)
- [x] `tests/test_models.py` — 각 모델 생성, 유효성 실패 케이스 테스트
- [x] Status 유효값 상수 정의

**완료 기준:** `pytest --cov=src --cov-report=term-missing` 커버리지 100%
**완료 후:** 사용자 승인 → git push

---

### Phase 2: Dummy 데이터 생성기 (Generator)

**목표:** 각 엔티티에 대해 무작위 유효 데이터를 생성하는 Generator 클래스 구현

**작업 목록:**
- [x] `src/generators.py`
  - `SampleGenerator.generate(count: int) -> list[Sample]`
  - `OrderGenerator.generate(count: int, sample_ids: list[str]) -> list[Order]`
  - `InventoryGenerator.generate(sample_ids: list[str]) -> list[Inventory]`
- [x] `tests/test_generators.py`
  - 생성된 데이터가 모델 유효성 조건을 만족하는지
  - count=0, count=1, count=N 경계값
  - sample_ids가 빈 리스트일 때 처리

**완료 기준:** `pytest --cov=src --cov-report=term-missing` 커버리지 100%
**완료 후:** 사용자 승인 → git push

---

### Phase 3: 파일 Writer (Append)

**목표:** 생성된 데이터를 JSON 파일에 누적 추가(append)하는 FileWriter 구현

**작업 목록:**
- [x] `src/file_writer.py`
  - `JsonFileWriter.append(file_path: str, data: dict) -> None`
  - 파일 없으면 새로 생성, 있으면 기존 배열에 추가
  - 데이터 타입별 키 구분: `"samples"`, `"orders"`, `"inventories"`
- [x] `tests/test_file_writer.py`
  - 신규 파일 생성 케이스
  - 기존 파일에 누적 추가 케이스
  - 빈 리스트 추가 케이스
  - 잘못된 경로 처리

**완료 기준:** `pytest --cov=src --cov-report=term-missing` 커버리지 100%
**완료 후:** 사용자 승인 → git push

---

### Phase 4: 통합 진입점 (Integration)

**목표:** 전체 흐름을 조율하는 `DummyDataGenerator` 클래스 + CLI 인터페이스

**작업 목록:**
- [x] `src/dummy_data_generator.py`
  - `DummyDataGenerator.generate_and_save(output_path: str, sample_count: int, order_count: int) -> None`
  - Generator → FileWriter 연결
- [x] `main.py` — CLI 진입점 (argparse)
- [x] `tests/test_dummy_data_generator.py` — 통합 테스트 (파일 실제 생성 확인)
- [x] 전체 커버리지 최종 점검

**완료 기준:** `pytest --cov=src --cov-report=term-missing` 커버리지 ~100%, `python main.py` 실행 확인
**완료 후:** 사용자 승인 → git push (최종)

---

## 진행 현황 (DummyDataGenerator PoC)

| Phase | 상태 |
|-------|------|
| Phase 1: 도메인 모델 | ✅ 완료 |
| Phase 2: Generator | ✅ 완료 |
| Phase 3: File Writer | ✅ 완료 |
| Phase 4: 통합 | ✅ 완료 |

---

# SampleOrderSystem 개발 진행 현황

## Phase 계획 및 완료 현황

| Phase | 내용 | 상태 |
|-------|------|------|
| Phase 1 | 프로젝트 기반 + 도메인 모델 (Sample, Order, Inventory, OrderStatus) | ✅ 완료 |
| Phase 2 | 데이터 영속성 (JSON Repository, BaseRepository[T]) | ✅ 완료 |
| Phase 3 | 시료 관리 메뉴 (MVC, BaseSampleView ABC) | ✅ 완료 |
| Phase 4 | 주문 접수/승인/거절 (OrderService, ProductionQueueProtocol) | ✅ 완료 |
| Phase 5 | 생산 라인 (ProductionCalculator, FIFO Queue, AbstractProductionQueue) | ✅ 완료 |
| Phase 6 | 모니터링 (InventoryStatusLabel Enum, ReadableRepository Protocol) | ✅ 완료 |
| Phase 7 | 출고 처리 (CONFIRMED → RELEASE) | ✅ 완료 |
| Phase 8 | 메인 메뉴 통합 + main.py | ✅ 완료 |
| Phase 9 | 생산 큐 영속성 및 재시작 복원 | 🔲 예정 |

## 누적 테스트 현황

| 항목 | 수치 |
|------|------|
| 전체 테스트 수 | 245개 |
| 커버리지 | 100% |
| 개발 방법론 | TDD (Red → Green → Refactor) |
