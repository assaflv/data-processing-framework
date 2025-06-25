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
    data_json_file.write_text('{"items": [{"a": 1}, {"a": 2}]}')
    reader = JSONFileReader(json_key="items")
    result = list(reader.read(str(data_json_file)))
    assert result[0] == [{"a": 1}, {"a": 2}]

def test_read_with_validation_schema(data_json_file):
    data_json_file.write_text('{"items": [{"a": 1}, {"a": 2}, {"a": "bad"}]}')
    reader = JSONFileReader(json_key="items.item", validation_schema=ItemModel)
    with pytest.raises(ValueError):
        list(reader.read(str(data_json_file)))