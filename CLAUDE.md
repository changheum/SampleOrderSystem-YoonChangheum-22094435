# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SampleOrderSystem** — 반도체 시료(Sample) 생산주문관리 시스템 for virtual company "S-Semi".
Python 기반 Console UI(MVC) 프로젝트. 모든 개발은 TDD로 진행한다.

## Commands

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=term-missing

# Run a single test file
pytest tests/test_models.py -v

# Run a single test by name
pytest tests/test_models.py::test_function_name -v

# Install dependencies
pip install -r requirements.txt
```

Coverage target: **~100%**. Each Phase is complete only when coverage meets the target.

## Architecture

The system integrates four verified PoC modules located at `C:\reviewer\Project\`:

| Module Path | Role |
|---|---|
| `ConsoleMVC-YoonChangheum-22094435\` | Console MVC skeleton — controllers, views, menu routing |
| `DataPersistence-YoonChangheum-22094435\` | JSON-based data persistence (read/write/append) |
| `DataMonitor-YoonChangheum-22094435\` | Monitoring and status display logic |
| `DummyDataGenerator-YoonChangheum-22094435\` | Test dummy data generation |

The target structure mirrors the DummyDataGenerator PoC pattern:
- `src/` — production code (models, services, controllers, views)
- `tests/` — pytest test files mirroring `src/`
- `main.py` — CLI entry point
- `requirements.txt` — `pytest`, `pytest-cov`

## Domain Model

Three core entities (Python `dataclass`):

| Entity | Fields |
|---|---|
| `Sample` | `sample_id: str`, `name: str`, `avg_production_time: int` (>0, minutes), `yield_rate: float` (0 < y ≤ 1) |
| `Order` | `order_id: str`, `sample_id: str`, `customer_name: str`, `quantity: int` (>0), `status: str` |
| `Inventory` | `sample_id: str`, `stock_quantity: int` (≥0) |

**Order Status FSM:**
```
RESERVED → [approve] → stock check → CONFIRMED (재고 충분)
                                   → PRODUCING (재고 부족) → CONFIRMED (생산 완료)
         → [reject]  → REJECTED
CONFIRMED → [출고]  → RELEASE
```
`REJECTED` is excluded from monitoring displays.

**Production formula:**
- 실 생산량: `ceil(부족분 / (yield_rate * 0.9))`
- 총 생산 시간: `avg_production_time * 실 생산량`
- 생산 큐 스케줄링: **FIFO**

**Inventory display states:** 여유 (충분) / 부족 (부족) / 고갈 (stock=0)

## TDD Workflow (Red → Green → Review)

Every feature follows this cycle — never write production code before a failing test:

1. **RED**: Define exact goal → create/update `Phase#.md` → user reviews plan before coding
2. **GREEN**: Write minimal code to pass the tests → confirm `pytest` actually passes
3. **REVIEW**: Run `code-quality-validator` agent → check SOLID compliance → refactor if needed

**Commit at each stage** (RED commit with failing test, GREEN commit with passing implementation, REVIEW commit after refactor).

**Phase gate**: Each Phase ends with user approval → then `git push`.
Phase plans are documented in `Phase1.md`, `Phase2.md`, etc. at the repo root.

## Available Agents

Invoke these agents at the appropriate TDD stage:

| Agent | When to use |
|---|---|
| `tdd-ocp-implementer` | Starting a new feature from PRD — full Red-Green-Refactor cycle with OCP design |
| `code-quality-validator` | After GREEN — validates SOLID principles, OCP, readability, test coverage (scores 1–10 per dimension) |
| `prd-compliance-reviewer` | After implementing a feature — maps code against `PRD.md` requirements |
| `planning-consistency-validator` | After completing planning docs — cross-document consistency check |

## SOLID Enforcement

`code-quality-validator` must be run after every meaningful implementation. It checks:
- **S**RP — one reason to change per class
- **O**CP — open for extension (abstractions/strategies), closed for modification
- **L**SP — subclasses substitutable for parent
- **I**SP — no fat interfaces
- **D**IP — high-level modules depend on abstractions, not concrete classes

OCP is especially critical: new order statuses, inventory states, or menu items must be addable by creating new classes, not modifying existing ones.

## Test Standards

- Test names: `should_[behavior]_when_[condition]` or `given_[ctx]_when_[action]_then_[outcome]`
- Structure: Arrange-Act-Assert (AAA)
- Each test covers exactly one behavior
- Use `unittest.mock` for external dependencies (file I/O, time)

## Key Business Rules (non-obvious)

- Production quantity uses a **safety buffer**: divide by `yield_rate * 0.9`, not just `yield_rate`
- `REJECTED` orders must never appear in monitoring or production queue views
- When approving an order, inventory deduction and status change are **atomic** — both happen or neither
- Production queue ordering is strictly **FIFO** — no priority overrides
