from core.abstract import DataWriter
import json


class JSONWriter(DataWriter):
    def __init__(self, destination_path: str, output_pattern: str = "results_batch_{counter}"):
        if not destination_path:
            raise ValueError("destination_path must be provided and cannot be empty.")
        self.destination_path = destination_path
        self.output_pattern = output_pattern

    def write(self, data: dict, batch_id: int) -> None:
        path = f"{self.destination_path}/{self.output_pattern.format(counter=batch_id)}.json"
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
        