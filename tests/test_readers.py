import pytest
from pydantic import BaseModel
from readers.json_reader import JSONFileReader


class ItemModel(BaseModel):
    a: int


@pytest.fixture
def data_json_file(tmp_path):
    return tmp_path / "data.json"


def test_read_non_json_file(tmp_path):
    file = tmp_path / "bad.csv"
    file.write_text("not a json")
    reader = JSONFileReader(json_key="value.item")
    with pytest.raises(ValueError):
        list(reader.read(str(file)))


def test_read_empty_json_key(data_json_file):
    data_json_file.write_text("{}")
    reader = JSONFileReader(json_key="")
    with pytest.raises(ValueError):
        list(reader.read(str(data_json_file)))


def test_read_without_validation_schema(data_json_file):
    data_json_file.write_text('{"value": [{"a": 1}, {"a": 2}]}')
    reader = JSONFileReader(json_key="value.item")
    result = list(reader.read(str(data_json_file)))
    assert result == [{"a": 1}, {"a": 2}]


def test_read_validation_schema(data_json_file):
    data_json_file.write_text('{"value": [{"a": 1}, {"a": 2}, {"b": 3}]}')
    reader = JSONFileReader(json_key="value.item", validation_schema=ItemModel)
    result = list(reader.read(str(data_json_file)))
    assert len(result) == 2
    assert isinstance(result[0], ItemModel)
    assert result[0].a == 1
    assert result[1].a == 2
