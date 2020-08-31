import pytest

from src.nlp import tokenizer

SENTENCES = "a" * 5
WAKACHIES = ["a" for i in range(5)]


@pytest.mark.parametrize("n", [1, 2, 3])
def test_to_ngram(n):
    # N-gram変換器テスト
    sentence_results = tokenizer.to_ngram(item=SENTENCES, n=n)
    for sr in sentence_results:
        assert len(sr) == n
        assert sr == "a" * n

    wakachi_results = tokenizer.to_ngram(item=WAKACHIES, n=n)
    for wr in wakachi_results:
        assert len(wr) == n
        assert wr == ["a" for i in range(n)]


@pytest.mark.parametrize("max_n", [1, 2, 3])
def test_to_ngrams(max_n):
    # 複数のN-gramパターンを取得するテスト
    sentence_results_multi_pattern = tokenizer.to_ngrams(item=SENTENCES, max_n=max_n)
    assert len(sentence_results_multi_pattern) == max_n
    for i, sentence_result in enumerate(sentence_results_multi_pattern):
        test_to_ngram(i + 1)

    wakachi_results_multi_pattern = tokenizer.to_ngrams(item=WAKACHIES, max_n=max_n)
    for i, wr in enumerate(wakachi_results_multi_pattern):
        test_to_ngram(i + 1)


@pytest.mark.parametrize("sentence", ["走れ、メロス"])
def test_wakachi(sentence):
    janome_midashi_wakachi_result = tokenizer.wakachi_by_janome(sentence=sentence, is_midashi=True)
    assert janome_midashi_wakachi_result == ["走れ", "、", "メロス"]

    janome_base_form_wakachi_result = tokenizer.wakachi_by_janome(sentence=sentence, is_midashi=False)
    assert janome_base_form_wakachi_result == ["走れる", "、", "メロス"]

    ginza_midashi_wakachi_result = tokenizer.wakachi_by_ginza(sentence=sentence, is_midashi=True)
    assert ginza_midashi_wakachi_result == ["走れ", "、", "メロス"]

    ginza_base_form_wakachi_result = tokenizer.wakachi_by_ginza(sentence=sentence, is_midashi=False)
    assert ginza_base_form_wakachi_result == ["走る", "、", "メロス"]

    sentence_piece_wakachi_result = tokenizer.wakachi_by_sentencepiece(sentence=sentence)
    assert sentence_piece_wakachi_result == ["▁", "走", "れ", "、", "メ", "ロス"]
