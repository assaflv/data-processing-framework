from core.data_process_framework import DataProcessFramework
from readers.json_reader import JSONFileReader
from transformer.user_transformer import UserTransformer
from models.user_model import User
from writers.json_writer import JSONWriter


def main():
    json_reader = JSONFileReader()
    user_transformer = UserTransformer()
    json_writer = JSONWriter()

    data_process = DataProcessFramework(
        reader=json_reader,
        transformer=user_transformer,
        writer=json_writer,
        validation_schema=User,
    )

    data_process.run(source_path="data/fake_users_part_1.json", destination_path="data/")


if __name__ == "__main__":
    main()
