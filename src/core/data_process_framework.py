from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time


import logging

from core.abstract import DataReader, DataTransformer, DataWriter


class DataProcessFramework:
    def __init__(
        self,
        reader: DataReader,
        transformer: DataTransformer,
        writer: DataWriter,
        batch_size: int = 987,
        max_workers: int = 4,
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

    def run(self, source_paths: list[str]):
        # Ensure that in the worst case all the reader threads can fill up to one full batch before the writer thread has a chance to pull anything.
        data_queue = Queue(maxsize=self.batch_size * self.max_workers)
        reader_count = len(source_paths)
        with ThreadPoolExecutor(max_workers=self.max_workers + 1) as executor:
            executor.submit(self._writer, data_queue, reader_count)

            for path in source_paths:
                executor.submit(self._reader, path, data_queue)

    def _reader(self, path, q: Queue):
        try:
            logging.info(f"[{time.time()}] Reader started for {path}")
            for raw_item in self.reader.read(path):
                item = self.transformer.transform(raw_item)
                if item is not None:
                    q.put(item)
            logging.info(f"[{time.time()}] Reader finished for {path}")

        except Exception as e:
            logging.error(f"[{time.time()}] Error in reader for {path}: {e}")
        finally:
            q.put(None)

    def _writer(self, q: Queue, reader_count: int):
        logging.info(f"[{time.time()}] Writer started")
        batch = []
        batch_id = 0
        done_readers = 0

        while done_readers < reader_count:
            item = q.get()
            if item is None:
                done_readers += 1
                continue

            batch.append(item)
            if len(batch) >= self.batch_size:
                logging.info(f"[{time.time()}] Writing batch {batch_id} of size {len(batch)}")
                self.writer.write(batch, batch_id)
                batch.clear()
                batch_id += 1

        if batch:
            logging.info(f"[{time.time()}] Writing final batch {batch_id} of size {len(batch)}")
            self.writer.write(batch, batch_id)

        logging.info(f"[{time.time()}] Writer finished")
