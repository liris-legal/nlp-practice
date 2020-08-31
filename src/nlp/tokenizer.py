from typing import List, Union

import janome
import spacy
from janome.tokenizer import Tokenizer as JanomeTokenizer
from torchtext.data.functional import load_sp_model, sentencepiece_tokenizer

from src.constants import SENTENCE_PIECE_MODEL_PATH
from src.utils import log_decorator

janome_tokenizer = JanomeTokenizer()
ginza_tokenizer = spacy.load("ja_ginza")

sp_model = load_sp_model(SENTENCE_PIECE_MODEL_PATH)
sp_tokens_generator = sentencepiece_tokenizer(sp_model)


@log_decorator
def wakachi_by_sentencepiece(sentence: str) -> List[str]:
    """SentencePieceを用いた分かち書き

    Parameters
    ----------
    sentence : str
        分かち書きしたい文章

    Returns
    -------
    List[str]
        分かち書き結果
    """
    return list(sp_tokens_generator([sentence]))[0]


@log_decorator
def tokenize_by_ginza(sentence: str) -> spacy.tokens.doc.Doc:
    """Ginzaを用いた形態素解析

    Parameters
    ----------
    sentence : str
        形態素解析したい文章

    Returns
    -------
    spacy.tokens.doc.Doc
        spacyのDocコンテナオブジェクト(https://spacy.io/api)
    """
    tokens = ginza_tokenizer(sentence)
    return tokens


@log_decorator
def wakachi_by_ginza(sentence: str, is_midashi: bool = True) -> List[str]:
    """Ginzaを用いた分かち書き

    Parameters
    ----------
    sentence : str
        分かち書きしたい文章
    is_midashi : bool, optional
        見出し語で分かち書きをする場合はTrue, by default True

    Returns
    -------
    List[str]
        分かち書き結果
    """
    tokens = tokenize_by_ginza(sentence)
    if is_midashi:
        return [token.orth_ for token in tokens]
    return [token.lemma_ for token in tokens]


@log_decorator
def tokenize_by_janome(sentence: str) -> List[janome.tokenizer.Token]:
    """Janomeを用いた形態素解析

    Parameters
    ----------
    sentence : str
        解析したい文章

    Returns
    -------
    List[janome.tokenizer.Token]
        形態素解析結果
    """
    return janome_tokenizer.tokenize(sentence)


@log_decorator
def wakachi_by_janome(sentence: str, is_midashi: bool = True) -> List[str]:
    """Janomeを用いた形態素解析

    Parameters
    ----------
    sentence : str
        解析したい文章
    is_midashi : bool, optional
        見出し語で分かち書きをする場合はTrue, by default True

    Returns
    -------
    List[str]
        分かち書き結果
    """
    if is_midashi:
        return list(janome_tokenizer.tokenize(sentence, wakati=True))

    tokens = tokenize_by_janome(sentence)
    return [t.base_form for t in tokens]


@log_decorator
def to_ngrams(item: Union[str, List[str]], max_n: int) -> List[List[str]]:
    """複数パターンのN-gram変換器

    Parameters
    ----------
    item : List[[Union[str, List[str]]]]
        N-gramに変換したいテキストや単語が入った2次元の配列
    max_n : int > 0
        N-gramのNに相当する数

    Returns
    -------
    List[List[str]]
        itemをN-gramに変換した結果
    """
    if max_n < 1:
        raise Exception(f"max_n > 0 (but max_n={max_n})")
    return [to_ngram(item, n) for n in range(1, max_n + 1)]


@log_decorator
def to_ngram(item: Union[str, List[str]], n: int) -> List[str]:
    """N-gram変換器

    Parameters
    ----------
    item : Union[str, List[str]]
        N-gramに変換したい文字列、または分かち書きのリスト
    n : int
        N-gramのNに相当する数

    Returns
    -------
    List[str]
        itemをN-gramに変換した結果
    """
    if n < 1:
        raise Exception(f"n > 0 (but n={n})")
    return [item[i: i + n] for i in range(len(item) - n + 1)]
