from abc import ABC, abstractmethod
import logging
from typing import Dict, Type, Union

from pydantic import BaseModel


class DataReader(ABC):
    @abstractmethod
    def read(self, source_path: str) -> Union[Type[BaseModel], Dict]:
        pass


class DataTransformer(ABC):
    @abstractmethod
    def transform(self, data: Union[Type[BaseModel], Dict]) -> Dict:
        pass


class DataWriter(ABC):
    @abstractmethod
    def write(self, data: Union[Type[BaseModel], Dict], output_path: str) -> None:
        pass
