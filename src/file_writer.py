import csv
from logging import getLogger
from typing import List

from src.utils import log_decorator

logger = getLogger()


@log_decorator
def write_in_separated_value_file(file_path: str, rows_list: List[List[str]], delimiter=",") -> None:
    """区切り文字で区切られたCSV、TSVなどのファイル書き込み

    Parameters
    ----------
    file_path : str
        ファイルパス
    rows_list : List[List[str]]
        ファイルに書き込む文字列を行ごとに格納した配列
    delimiter : str, optional
        区切り文字, by default ","
    """
    with open(file_path, "w") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(rows_list)
