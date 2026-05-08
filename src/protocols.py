from typing import Protocol
from src.models import Order, Sample


class ProductionQueueProtocol(Protocol):
    def enqueue(self, order: Order, sample: Sample) -> None: ...
