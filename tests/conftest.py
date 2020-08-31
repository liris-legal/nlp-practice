import os

TEST_DATA_PATH = os.path.join(os.getenv("APP_PATH", "/app"), "tests/test_data")

TEST_JSON_PATH = os.path.join(TEST_DATA_PATH, "test_read.json")
TEST_CSV_PATH = os.path.join(TEST_DATA_PATH, "test_read.csv")
TEST_TSV_PATH = os.path.join(TEST_DATA_PATH, "test_read.tsv")
TEST_PDF_PATH = os.path.join(TEST_DATA_PATH, "test_read.pdf")
TEST_DOCX_PATH = os.path.join(TEST_DATA_PATH, "test_read.docx")

TEST_WRITE_CSV_PATH = os.path.join(TEST_DATA_PATH, "test_write.csv")
TEST_WRITE_TSV_PATH = os.path.join(TEST_DATA_PATH, "test_write.tsv")
