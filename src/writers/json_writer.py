from core.ABC.data_writer import DataWriter
import json


class JSONWriter(DataWriter):
    def write(self, data: dict, file_path: str) -> None:
        """Write the content to a JSON file."""

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
