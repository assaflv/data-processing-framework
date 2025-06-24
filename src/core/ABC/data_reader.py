from abc import ABC, abstractmethod


class DataReader(ABC):
    @abstractmethod
    def read(self, source_path: str) -> str:
        """
        Reads data from the specified source path.

        """
        pass
