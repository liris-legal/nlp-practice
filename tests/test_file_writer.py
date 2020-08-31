import os

import pytest
from tests.conftest import TEST_CSV_PATH, TEST_WRITE_CSV_PATH, TEST_WRITE_TSV_PATH

from src import file_reader, file_writer


@pytest.mark.parametrize("path, delimiter", [(TEST_WRITE_CSV_PATH, ","), (TEST_WRITE_TSV_PATH, "\t")])
def test_write_in_separated_value_file(path, delimiter):
    csv_rows = file_reader.read_csv(TEST_CSV_PATH)
    if os.path.exists(path):
        os.remove(path)
    file_writer.write_in_separated_value_file(path, csv_rows, delimiter)
    assert os.path.exists(path) is True
