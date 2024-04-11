from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel


class BaseClassConfig:
    populate_by_name = True


class BaseData(BaseModel):
    class Config(BaseClassConfig):
        pass


Output = TypeVar("Output", bound=BaseData)
Input = TypeVar("Input", bound=BaseData)


class Usecase(ABC, Generic[Input, Output]):
    @abstractmethod
    def execute(self, data: Input) -> Output:
        raise NotImplementedError()
