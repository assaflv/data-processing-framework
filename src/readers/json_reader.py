from core.ABC.data_reader import DataReader

import os
import ijson


class JSONFileReader(DataReader):
    def read(self, source_path: str):
        """Read the content of a JSON file and return it as a dictionary."""

        if not os.path.exists(source_path):
            raise FileNotFoundError(f"The file {source_path} does not exist.")
        if not source_path.endswith(".json"):
            raise ValueError("The provided file is not a JSON file.")

        try:
            with open(source_path, "r") as file:
                for obj in ijson.items(file, "value.item"):
                    print(f"Reading object: {obj}")  # Debug statement
                    yield obj
        except ijson.IncompleteJSONError as e:
            raise ValueError(f"Error decoding JSON from file {source_path}: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred while reading the file {source_path}: {e}")
