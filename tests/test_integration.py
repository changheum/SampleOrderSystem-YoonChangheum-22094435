"""
전체 주문 흐름 통합 테스트.
실제 JSON Repository를 임시 파일로 사용하여 계층 간 연결을 검증한다.
"""
import pytest
from src.models import OrderStatus
from src.json_repository import JsonSampleRepository, JsonOrderRepository, JsonInventoryRepository
from src.production_queue import ProductionQueue
from src.production_calculator import ProductionCalculator
from src.sample_service import SampleService
from src.order_service import OrderService
from src.production_service import ProductionService
from src.release_service import ReleaseService
from src.monitoring_service import MonitoringService, InventoryStatusLabel


@pytest.fixture
def repos(tmp_path):
    return {
        "sample": JsonSampleRepository(str(tmp_path / "samples.json")),
        "order": JsonOrderRepository(str(tmp_path / "orders.json")),
        "inventory": JsonInventoryRepository(str(tmp_path / "inventories.json")),
    }


@pytest.fixture
def queue():
    return ProductionQueue()


@pytest.fixture
def services(repos, queue):
    sample_svc = SampleService(repos["sample"], repos["inventory"])
    order_svc = OrderService(repos["order"], repos["sample"], repos["inventory"], queue)
    production_svc = ProductionService(repos["order"], repos["inventory"], queue)
    release_svc = ReleaseService(repos["order"])
    monitoring_svc = MonitoringService(repos["order"], repos["sample"], repos["inventory"])
    return {
        "sample": sample_svc,
        "order": order_svc,
        "production": production_svc,
        "release": release_svc,
        "monitoring": monitoring_svc,
    }


class TestIntegrationStockSufficientFlow:
    def test_full_flow_reserved_to_release(self, services):
        """접수 → 승인(재고 충분) → 출고 전체 흐름"""
        sample_svc = services["sample"]
        order_svc = services["order"]
        release_svc = services["release"]

        # 시료 등록 + 재고 보충
        sample_svc.register("S001", "GaN Wafer", 60, 0.9)
        from src.models import Inventory
        from src.json_repository import JsonInventoryRepository
        inv_repo = services["sample"]._inventory_repo
        inv_repo.save(Inventory(sample_id="S001", stock_quantity=100))

        # 주문 접수
        order = order_svc.place_order("S001", "KAIST Lab", 10)
        assert order.status == OrderStatus.RESERVED

        # 승인 → 재고 충분 → CONFIRMED
        confirmed = order_svc.approve(order.order_id)
        assert confirmed.status == OrderStatus.CONFIRMED

        # 재고 차감 확인
        inv = inv_repo.find_by_id("S001")
        assert inv.stock_quantity == 90

        # 출고
        released = release_svc.release(confirmed.order_id)
        assert released.status == OrderStatus.RELEASE


class TestIntegrationStockInsufficientFlow:
    def test_full_flow_reserved_to_producing_to_confirmed(self, services, queue):
        """접수 → 승인(재고 부족) → 생산 완료 → 출고 전체 흐름"""
        sample_svc = services["sample"]
        order_svc = services["order"]
        production_svc = services["production"]
        release_svc = services["release"]

        sample_svc.register("S001", "GaN Wafer", 60, 0.9)

        # 주문 접수 (재고 0)
        order = order_svc.place_order("S001", "KAIST Lab", 10)

        # 승인 → 재고 부족 → PRODUCING
        producing = order_svc.approve(order.order_id)
        assert producing.status == OrderStatus.PRODUCING

        # 생산 큐에 작업 등록 확인
        job = production_svc.get_current_job()
        assert job is not None
        assert job.order_id == producing.order_id

        # 생산 완료 → CONFIRMED
        confirmed = production_svc.complete_job(job.job_id)
        assert confirmed.status == OrderStatus.CONFIRMED

        # 출고
        released = release_svc.release(confirmed.order_id)
        assert released.status == OrderStatus.RELEASE


class TestIntegrationRejectFlow:
    def test_rejected_order_not_in_monitoring(self, services):
        """접수 → 거절 → 모니터링 미표시"""
        sample_svc = services["sample"]
        order_svc = services["order"]
        monitoring_svc = services["monitoring"]

        sample_svc.register("S001", "GaN Wafer", 60, 0.9)
        order = order_svc.place_order("S001", "KAIST Lab", 10)
        order_svc.reject(order.order_id)

        result = monitoring_svc.get_orders_by_status()
        assert OrderStatus.REJECTED not in result
        all_visible = [o for orders in result.values() for o in orders]
        assert all(o.status != OrderStatus.REJECTED for o in all_visible)


class TestIntegrationMonitoring:
    def test_inventory_status_reflects_orders(self, services):
        """주문 수량 대비 재고 상태 반영 확인"""
        sample_svc = services["sample"]
        order_svc = services["order"]
        monitoring_svc = services["monitoring"]
        from src.models import Inventory

        sample_svc.register("S001", "GaN Wafer", 60, 0.9)
        inv_repo = sample_svc._inventory_repo
        inv_repo.save(Inventory(sample_id="S001", stock_quantity=5))

        order_svc.place_order("S001", "KAIST Lab", 100)

        status_list = monitoring_svc.get_inventory_status()
        assert status_list[0]["status"] == InventoryStatusLabel.SHORTAGE
