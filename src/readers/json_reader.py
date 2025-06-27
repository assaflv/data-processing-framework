import logging
import os
from typing import Generator, Optional, Type, Union
import ijson
from pydantic import BaseModel, ValidationError

from core.abstract import DataReader


class JSONFileReader(DataReader):
    def __init__(
        self,
        json_key: str,
        validation_schema: Optional[Type[BaseModel]] = None,
    ):
        self.json_key = json_key
        self.validation_schema = validation_schema

    def read(self, source_path: str) -> Generator[Union[Type[BaseModel], dict]]:
        if not self.json_key:
            raise ValueError("json_key must be provided and cannot be empty.")
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"The file {source_path} does not exist.")
        if not source_path.endswith(".json"):
            raise ValueError("The provided file is not a JSON file.")

        try:
            with open(source_path, "r") as file:
                for obj in ijson.items(file, self.json_key):
                    if self.validation_schema:
                        try:
                            validate = self.validation_schema(**obj)
                            yield validate
                        except ValidationError as e:
                            logging.error(f"Validation error: {e} for data id: {obj}")
                            continue
                    else:
                        yield obj
        except ijson.IncompleteJSONError as e:
            raise ValueError(f"Error decoding JSON from file {source_path}: {e}")
        except ValueError as e:
            raise ValueError(f"Value error while reading '{source_path}': {e}") from e
        except Exception as e:
            raise RuntimeError(f"An error occurred while reading the file {source_path}: {e}")
