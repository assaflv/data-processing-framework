from core.abstract import DataReader, DataTransformer, DataWriter
from core.data_process_framework import DataProcessFramework


class DummyReader(DataReader):
    def read(self, path):
        return [f"{path}_item1", f"{path}_item2"]


class DummyTransformer(DataTransformer):
    def transform(self, item):
        return item.upper()


class DummyWriter(DataWriter):
    def __init__(self):
        self.batches = []

    def write(self, batch, batch_id):
        self.batches.append((batch_id, list(batch)))


def test_data_process_framework_basic(monkeypatch):
    reader = DummyReader()
    transformer = DummyTransformer()
    writer = DummyWriter()
    framework = DataProcessFramework(
        reader=reader,
        transformer=transformer,
        writer=writer,
        batch_size=2,
        max_workers=2,
    )
    source_paths = ["fileA", "fileB"]
    framework.run(source_paths)

    all_items = [item for batch_id, batch in writer.batches for item in batch]
    assert sorted(all_items) == ["FILEA_ITEM1", "FILEA_ITEM2", "FILEB_ITEM1", "FILEB_ITEM2"]
    assert len(writer.batches) == 2
