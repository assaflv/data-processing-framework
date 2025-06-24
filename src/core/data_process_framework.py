from typing import Dict, Optional, Type, Union
from pydantic import BaseModel
from pydantic_core import ValidationError
from core.ABC.data_reader import DataReader
from core.ABC.data_transformer import DataTransformer
from core.ABC.data_writer import DataWriter
import logging


class DataProcessFramework:
    def __init__(
        self,
        reader: DataReader,
        transformer: DataTransformer,
        writer: DataWriter,
        validation_schema: Optional[Type[BaseModel]] = None,
        batch_size: int = 1000,
        output_pattern: str = "results_batch_{counter}",
        single_batch_filename: str = "results",
    ):
        if not isinstance(reader, DataReader):
            raise TypeError("reader must be an instance of DataReader")
        if not isinstance(transformer, DataTransformer):
            raise TypeError("transformer must be an instance of DataTransformer")
        if not isinstance(writer, DataWriter):
            raise TypeError("writer must be an instance of DataWriter")

        self.reader = reader
        self.transformer = transformer
        self.writer = writer
        self.schema = validation_schema
        self.batch_size = batch_size
        self.output_pattern = f"{output_pattern}.json"
        self.single_batch_filename = f"{single_batch_filename}.json"

    def run(self, source_path: str, destination_path: str):
        """Run the data processing pipeline."""

        data = self.reader.read(source_path)
        batch_counter = 0
        transformed_items = []
        for item in data:
            if self.schema:
                try:
                    processed_item = self.schema(**item)
                except ValidationError as e:
                    print(f"Validation error for item {item}: {e}")
                    continue
            else:
                processed_item = item

            transformed_data = self.transformer.transform(processed_item)

            transformed_items.append(transformed_data)

            if len(transformed_items) >= self.batch_size:
                self._write(transformed_items, batch_counter)

                batch_counter += 1
                transformed_items = []
        if transformed_items:
            self._write(transformed_items, batch_counter, one_batch_flag=(batch_counter == 0))

    def _write(self, data: Union[Dict, Type[BaseModel]], counter: int, one_batch_flag: bool = False):
        output_file = self.single_batch_filename if one_batch_flag else self.output_pattern.format(counter=counter)
        self.writer.write(
            data,
            output_file,
        )

        logging.info(f"writing {len(data)} items to {output_file}")

        self.writer.write(data, output_file)
