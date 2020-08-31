from tests.conftest import TEST_CSV_PATH, TEST_DOCX_PATH, TEST_JSON_PATH, TEST_PDF_PATH, TEST_TSV_PATH

from src import file_reader


def test_read_json():
    results = file_reader.read_json(TEST_JSON_PATH)
    for i, r in enumerate(results):
        assert r["id"] == i


def test_read_csv():
    results = file_reader.read_csv(TEST_CSV_PATH)
    assert len(results) == 6
    for i, r in enumerate(results):
        assert r[0] == str(i)
        if i == 0:
            assert r[1] == "a"
        if i == 1:
            assert r[1] == "b"
        if i == 2:
            assert r[1] == "c"


def test_read_tsv():
    results = file_reader.read_tsv(TEST_TSV_PATH)
    assert len(results) == 6
    for i, r in enumerate(results):
        assert r[0] == str(i)
        if i == 0:
            assert r[1] == "a"
        if i == 1:
            assert r[1] == "b"
        if i == 2:
            assert r[1] == "c"


def test_read_pdf():
    results = file_reader.read_pdf_text(TEST_PDF_PATH)
    assert (isinstance(results, list) and all(isinstance(x, str) for x in results)) is True
    assert len(results) > 0


def test_read_docx():
    results = file_reader.read_docx_text(TEST_DOCX_PATH)
    assert (isinstance(results, list) and all(isinstance(x, str) for x in results)) is True
    assert len(results) > 0
