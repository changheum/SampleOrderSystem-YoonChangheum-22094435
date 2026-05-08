from src.json_repository import JsonSampleRepository, JsonOrderRepository, JsonInventoryRepository
from src.production_queue import ProductionQueue
from src.sample_service import SampleService
from src.order_service import OrderService
from src.production_service import ProductionService
from src.release_service import ReleaseService
from src.monitoring_service import MonitoringService
from src.controllers.sample_controller import SampleController
from src.controllers.order_controller import OrderController
from src.controllers.monitoring_controller import MonitoringController
from src.controllers.production_controller import ProductionController
from src.controllers.release_controller import ReleaseController
from src.main_menu import MainMenu

DATA_DIR = "data"

def main():
    import os
    os.makedirs(DATA_DIR, exist_ok=True)

    sample_repo    = JsonSampleRepository(f"{DATA_DIR}/samples.json")
    order_repo     = JsonOrderRepository(f"{DATA_DIR}/orders.json")
    inventory_repo = JsonInventoryRepository(f"{DATA_DIR}/inventories.json")
    queue          = ProductionQueue()

    sample_svc     = SampleService(sample_repo, inventory_repo)
    order_svc      = OrderService(order_repo, sample_repo, inventory_repo, queue)
    production_svc = ProductionService(order_repo, inventory_repo, queue)
    release_svc    = ReleaseService(order_repo)
    monitoring_svc = MonitoringService(order_repo, sample_repo, inventory_repo)

    menu = MainMenu(
        sample_ctrl     = SampleController(sample_svc),
        order_ctrl      = OrderController(order_svc, sample_svc),
        monitoring_ctrl = MonitoringController(monitoring_svc),
        production_ctrl = ProductionController(production_svc),
        release_ctrl    = ReleaseController(release_svc),
    )
    menu.run()


if __name__ == "__main__":
    main()
