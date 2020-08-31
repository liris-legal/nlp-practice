import pytest

from src.nlp import normalizer


@pytest.mark.parametrize("sentence, replacement", [("100", "0"), ("3,000", ""), ("5,000,000", "_数字_"), ("７００,０００", "あ")])
def test_normalize_numbers(sentence, replacement):
    sufix = "円"
    test_sentence = sentence + sufix
    result = normalizer.normalize_numbers(sentence=test_sentence, replacement=replacement)
    assert result == replacement + sufix


@pytest.mark.parametrize("sentence, replacement, do_strip", [
    ("ス  ペー   ス", "", True), ("  スペース ", "", True)])
def test_normalize_spaces(sentence, replacement, do_strip):
    result = normalizer.normalize_spaces(sentence=sentence, replacement=replacement, do_strip=do_strip)
    assert result == "スペース"
