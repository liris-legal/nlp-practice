import contextlib
import csv
import json
from io import StringIO
from typing import Dict, List, Union

from chardet.universaldetector import UniversalDetector
from docx import Document
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

from src.utils import check_read_file_decorator, log_decorator


@check_read_file_decorator("json")
@log_decorator
def read_json(file_path: str) -> dict:
    """JSONファイルの読み込み

    Parameters
    ----------
    file_path : str
        ファイルパス

    Returns
    -------
    dict
        Jsonファイルを読み込んだ結果
    """
    encoding = detect_encoding(file_path=file_path)['encoding']
    result = None
    with open(file_path, "r", encoding=encoding) as f:
        result = json.load(f)
    return result


@log_decorator
def read_separated_value_file(file_path: str, delimiter: str = ",") -> List[List[str]]:
    """CSVやTSVなど区切り文字で区切られたテキストファイルをdelimiterで分割し、2次元配列として返す

    Parameters
    ----------
    file_path : str
        ファイルパス
    delimiter : str, optional
        区切り文字, by default ','

    Returns
    -------
    List[List[str]]
        ファイル内のテキストをdelimiterで分割した2次元配列
    """

    encoding = detect_encoding(file_path=file_path)['encoding']
    with open(file_path, "r", encoding=encoding) as f:
        reader = csv.reader(f, delimiter=delimiter)
        return [row for row in reader]


@check_read_file_decorator("csv")
@log_decorator
def read_csv(file_path: str) -> List[List[str]]:
    """CSVファイルを読み込み、2次元の配列で取得

    Parameters
    ----------
    file_path : str
        ファイルパス

    Returns
    -------
    List[List[str]]
        CSV読み込みの結果の2次元の文字列配列
    """

    return read_separated_value_file(file_path=file_path, delimiter=",")


@check_read_file_decorator("tsv")
@log_decorator
def read_tsv(file_path: str) -> List[List[str]]:
    """TSVファイルを読み込み、2次元の配列で取得

    Parameters
    ----------
    file_path : str
        ファイルパス

    Returns
    -------
    List[List[str]]
        TSV読み込みの結果の2次元の文字列配列
    """

    return read_separated_value_file(file_path=file_path, delimiter="\t")


@check_read_file_decorator("pdf")
@log_decorator
def read_pdf_text(file_path: str, password: str = None) -> List[str]:
    """PDFファイルからテキストを読み込む

    Parameters
    ----------
    file_path : str
        ファイルパス
    password : str, optional
        PDFファイルにパスワードがかかっている場合はそのパスワード, by default None

    Returns
    -------
    List[str]
        抽出したPDFのテキスト情報
    """

    with open(file_path, "rb") as f:
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        device = TextConverter(rsrcmgr, retstr, codec="utf-8", laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(f, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
            interpreter.process_page(page)

        pdf_text = retstr.getvalue()

        device.close()
        retstr.close()

    return pdf_text


@check_read_file_decorator("docx")
@log_decorator
def read_docx_text(file_path: str) -> List[str]:
    """docxのWordファイルの読み込み

    Parameters
    ----------
    file_path : str
        ファイルパス

    Returns
    -------
    List[str]
        docxを段落ごとに分割して読み込んだ結果
    """
    with open(file_path, "rb") as f:
        doc = Document(f)
        return [par.text for par in doc.paragraphs if par.text]


@check_read_file_decorator('txt')
@log_decorator
def read_txt(file_path: str) -> str:
    """txtファイルの読み込み
    - エンコード方式は自動で検出

    Parameters
    ----------
    file_path : str
        読み込む対象のファイルパス

    Returns
    -------
    str
        テキストファイルを読み込んだ結果
    """

    encoding = detect_encoding(file_path=file_path)['encoding']
    with open(file_path, 'r', encoding=encoding) as f:
        text = f.read()
    return text


@log_decorator
def detect_encoding(file_path: str, chunk_size: int = 100) -> Dict[str, Union[str, float]]:
    """エンコード方式を自動で検出
    - 大容量ファイルに対応するため細かくファイルを分割して分析

    Parameters
    ----------
    file_path : str
        対象のファイルパス
    chunk_size : int, optional
        1回の分析の最大容量（Byte単位）, by default 100

    Returns
    -------
    Dict[str, Union[str, float]]
        {'encoding': 'エンコード内容', 'confidence': '検出の確度'}
    """

    with open(file_path, "rb") as f, contextlib.closing(UniversalDetector()) as detector:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            detector.feed(chunk)
            if detector.done:
                break
    return detector.result
