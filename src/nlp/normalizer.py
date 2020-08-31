import re

import mojimoji

from src.utils import log_decorator

normalize_numbers_default_pattern = re.compile(r"(\d+[,，]*)+")
normalize_spaces_default_pattern = re.compile(r"\s+")


@log_decorator
def normalize_numbers(sentence: str, replacement: str = "0", pattern: str = None) -> str:
    """正規表現patternに該当する数字をreplacementに置換する

    Parameters
    ----------
    sentence : str
        処理したい文章
    replacement : str, optional
        処理後の置換文字列, by default "0"
    pattern : str, optional
        処理したい正規表現のパターン
        Noneの場合はデフォルトパターン"(\d+[,，]*)+"で処理, by default None

    Returns
    -------
    str
        数字正規化処理後の文字列
    """

    if not pattern:
        pattern = normalize_numbers_default_pattern
    hankaku_num_sentence = mojimoji.zen_to_han(sentence, kana=False, digit=True, ascii=False)
    return re.sub(pattern, replacement, hankaku_num_sentence)


@log_decorator
def normalize_spaces(sentence: str, replacement: str = "", pattern: str = None, do_strip: bool = True) -> str:
    """正規表現patternに該当する空白文字をreplacementに置換する

    Parameters
    ----------
    sentence : str
        処理したい文章
    replacement : str, optional
        処理後の置換文字列, by default ""
    pattern : str, optional
        処理したい正規表現のパターン
        Noneの場合はデフォルトパターン'\s+'で処理, by default None
    do_strip : bool, optional
        sentence前後の空白文字を自動で除去するかどうか, by default True

    Returns
    -------
    str
        空白文字正規化後の文字列
    """
    if not pattern:
        pattern = normalize_spaces_default_pattern
    proc_sentence = sentence
    if do_strip:
        proc_sentence = proc_sentence.strip()
    return re.sub(pattern, replacement, proc_sentence)
