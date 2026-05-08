from src.models import Sample, Inventory
from src.repository import SampleRepository, InventoryRepository


class SampleService:
    def __init__(self, sample_repo: SampleRepository, inventory_repo: InventoryRepository):
        self._sample_repo = sample_repo
        self._inventory_repo = inventory_repo

    def register(self, sample_id: str, name: str, avg_production_time: int, yield_rate: float) -> Sample:
        if self._sample_repo.find_by_id(sample_id) is not None:
            raise ValueError(f"Sample '{sample_id}' already exists")
        sample = Sample(
            sample_id=sample_id,
            name=name,
            avg_production_time=avg_production_time,
            yield_rate=yield_rate,
        )
        self._sample_repo.save(sample)
        self._inventory_repo.save(Inventory(sample_id=sample_id, stock_quantity=0))
        return sample

    def find_all(self) -> list[dict]:
        return [self._to_entry(s) for s in self._sample_repo.find_all()]

    def search_by_name(self, keyword: str) -> list[dict]:
        return [
            self._to_entry(s)
            for s in self._sample_repo.find_all()
            if keyword.lower() in s.name.lower()
        ]

    def _to_entry(self, sample: Sample) -> dict:
        inventory = self._inventory_repo.find_by_id(sample.sample_id)
        stock = inventory.stock_quantity if inventory else 0
        return {"sample": sample, "stock_quantity": stock}
