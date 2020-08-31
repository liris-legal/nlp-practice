import logging.config
import os
import sys
from inspect import getframeinfo, stack
from logging import getLogger
from typing import Callable

logging.config.fileConfig(os.getenv("LOG_CONF_PATH"))
logger = getLogger(__name__)


def paramdeco(func: Callable) -> Callable:
    """引数ありのデコレータを書きやすくするためのデコレータ

    Parameters
    ----------
    func : Callable
        引数を渡したい任意のデコレータ関数

    Returns
    -------
    Callable
        引数ありの任意の関数
    """

    def param(*args, **kwargs):
        def wrapper(f):
            return func(f, *args, **kwargs)

        return wrapper

    return param


def log_decorator(func: Callable) -> Callable:
    caller = getframeinfo(stack()[1][0])

    def wrapper(*args, **kwargs):
        try:
            logger.debug(f"{caller.filename}:L{caller.lineno} | {func.__name__} | {args} | {kwargs} | start")
            result = func(*args, **kwargs)
            logger.debug(f"{caller.filename}:L{caller.lineno} | {func.__name__} | {args} | {kwargs} | completed")
            return result
        except Exception as e:
            logger.error(f"{caller.filename}:L{caller.lineno} | {func.__name__} | {args} | {kwargs} | {e}")
            sys.exit(1)

    return wrapper


@paramdeco
def check_read_file_decorator(func: Callable, extension: str = None) -> Callable:
    """ファイル処理の前にファイルの拡張子などを確認するデコレータ

    Parameters
    ----------
    func : Callable
        任意の関数
    extension : str
        拡張子（example: pdf, txt, csv, tsv）

    Returns
    -------
    wrapper : Callable
        ラッパー関数
    """

    def wrapper(*args, **kwargs):
        is_exist_file_path(*args, **kwargs)
        if extension:
            is_match_extension(extension=extension, *args, **kwargs)
        return func(*args, **kwargs)

    return wrapper


@log_decorator
def is_match_extension(file_path: str, extension: str) -> None:
    """file_path内の拡張子がextensionと一致するかを確認

    Parameters
    ----------
    file_path : str
        ファイルパス
    extension : str
        拡張子（'.'無し）

    Raises
    ------
    Exception
        file_path内の拡張子がextensionと一致しない場合エラーをraiseし、プログラムを停止する
    """

    _, ext = os.path.splitext(file_path)
    if ext != f".{extension}":
        raise Exception(f"file_path: {file_path} の拡張子が{extension}ではありません")


@log_decorator
def is_exist_file_path(file_path: str, *args, **kwargs) -> None:
    """ファイルパスが存在するかどうかを確認

    Parameters
    ----------
    file_path : str
        ファイルパス

    Raises
    ------
    Exception
        ファイルパスが存在しない場合エラーをraiseし、プログラムを停止する
    """
    if not os.path.exists(file_path):
        raise Exception(f"file_path: {file_path} は存在しません")
