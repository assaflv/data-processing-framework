from abc import ABC, abstractmethod


class DataTransformer(ABC):
    @abstractmethod
    def transform(self, data):
        pass
