import os
from core.data_process_framework import DataProcessFramework
from readers.json_reader import JSONFileReader
from transformer.user_transformer import UserTransformer
from models.user_input_model import UserInput
from writers.json_writer import JSONWriter
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main():
    output_path = "data/output"
    if not os.path.exists(output_path):
        raise FileNotFoundError(
            f"Output directory '{output_path}' does not exist. Please create it before running the program."
        )

    json_reader = JSONFileReader(json_key="value.item", validation_schema=UserInput)
    user_transformer = UserTransformer()
    json_writer = JSONWriter(
        destination_path=output_path,
    )

    data_process = DataProcessFramework(
        reader=json_reader,
        transformer=user_transformer,
        writer=json_writer,
    )

    source_paths = [
        "data/fake_users_part_1.json",
        "data/fake_users_part_2.json",
        "data/fake_users_part_3.json",
        "data/fake_users_part_4.json",
    ]

    data_process.run(source_paths=source_paths)


if __name__ == "__main__":
    main()
