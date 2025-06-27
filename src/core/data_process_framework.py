from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time


import logging

from core.abstract import DataReader, DataTransformer, DataWriter

_sentinel = object()


class DataProcessFramework:
    def __init__(
        self,
        reader: DataReader,
        transformer: DataTransformer,
        writer: DataWriter,
        batch_size: int = 987,
        max_workers: int = None,
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
        self.batch_size = batch_size
        self.max_workers = max_workers
        self.total_writing_items = 0

    def run(self, source_paths: list[str]):
        data_queue = Queue()
        reader_count = len(source_paths)

        if self.max_workers is None:
            self.max_workers = reader_count

        with ThreadPoolExecutor(max_workers=self.max_workers + 1) as executor:
            executor.submit(self._writer, data_queue, reader_count)

            for path in source_paths:
                executor.submit(self._reader, path, data_queue)

    def _reader(self, path, q: Queue):
        try:
            for raw_item in self.reader.read(path):
                try:
                    item = self.transformer.transform(raw_item)
                    q.put(item)
                except Exception as e:
                    logging.error(f"[{time.time()}] Error transforming item from {path}: {e}")

        except Exception as e:
            logging.error(f"[{time.time()}] Error in reader for {path}: {e}")
        finally:
            q.put(_sentinel)

    def _writer(self, q: Queue, reader_count: int):
        logging.info(f"[{time.time()}] Writer started")
        batch = []
        batch_id = 0
        done_readers = 0

        while done_readers < reader_count:
            item = q.get()
            if item is _sentinel:
                done_readers += 1
                continue

            batch.append(item)
            if len(batch) >= self.batch_size:
                self._write(batch, batch_id)
                batch.clear()
                batch_id += 1

        if batch:
            self._write(batch, batch_id)
        logging.info(f"[{time.time()}] Writer finished, total items written: {self.total_writing_items}")

    def _write(self, batch: list, batch_id: int):
        logging.info(f"[{time.time()}] Writing batch {batch_id} of size {len(batch)}")
        self.writer.write(batch, batch_id)
        self.total_writing_items += len(batch)
