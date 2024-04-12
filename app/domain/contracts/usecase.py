from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.domain.entities.entity import Entity

# from pydantic import BaseModel


Output = TypeVar("Output", bound=Entity | None)
Input = TypeVar("Input", bound=Entity | None)


class Usecase(ABC, Generic[Input, Output]):
    @abstractmethod
    def execute(self, data: Input) -> Output:
        raise NotImplementedError()
