from abc import ABC, abstractmethod
from typing import Dict, Type, Union

from pydantic import BaseModel


class DataReader(ABC):
    def __init__(self, validation_schema: Type[BaseModel] = None):
        self.validation_schema = validation_schema

    def validate_data(self, data: Dict) -> Union[Type[BaseModel], Dict]:
        if self.validation_schema:
            try:
                return self.validation_schema(**data)
            except Exception as e:
                raise ValueError(f"Validation error: {e}")
        return data

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
