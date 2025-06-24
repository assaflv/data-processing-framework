from abc import ABC, abstractmethod


class DataWriter(ABC):
    @abstractmethod
    def write(self, data: str, output_path: str) -> None:
        """Write the content to a file"""
        pass
