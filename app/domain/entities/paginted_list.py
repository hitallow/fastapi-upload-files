from typing import Generic, List, TypeVar

from app.domain.entities.entity import Entity

T = TypeVar("T", bound=Entity)


class PaginatedEntities(Entity, Generic[T]):
    total_items: int
    items: List[T]
