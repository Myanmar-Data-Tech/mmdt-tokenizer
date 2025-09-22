import pytest
from mmdt_tokenizer.core import MyanmarTokenizer

@pytest.fixture(scope="module")
def tokenizer():
    """Provide a shared tokenizer instance for tests."""
    return MyanmarTokenizer(
        space_remove_mode="my_not_num",
        use_bimm_fallback=True,
        max_word_len=6
    )


def test_word_tokenize_basic(tokenizer):
    text = "မင်္ဂလာပါ လူကြီးမင်းတို့"
    tokens = tokenizer.word_tokenize(text)
    print(tokens)
    assert isinstance(tokens, list)
    assert "မင်္ဂလာပါ" in tokens or "မင်္ဂလာ" in tokens  


def test_word_tokenize_with_numbers(tokenizer):
    text = "အိမ် ၁၂ လုံး"
    tokens = tokenizer.word_tokenize(text)
    assert any(tok.isdigit() or "၁၂" in tok for tok in tokens)


def test_word_tokenize_with_english(tokenizer):
    text = "Yangon 2025"
    tokens = tokenizer.word_tokenize(text)
    assert "Yangon" in tokens
    assert any("2025" in tok for tok in tokens)


def test_syllable_tokenize_basic(tokenizer):
    text = "မင်္ဂလာပါ"
    tokens = tokenizer.syllable_tokenize(text)
    assert isinstance(tokens, list)
    assert any("မင်္" in tok or "ဂ" in tok for tok in tokens)

"""
def test_list_input(tokenizer):
    texts = ["မင်္ဂလာပါ", "ရန်ကုန်မြို့"]
    results = tokenizer.word_tokenize(texts)
    assert isinstance(results, list)
    assert isinstance(results[0], list)


def test_empty_string(tokenizer):
    text = ""
    tokens = tokenizer.word_tokenize(text)
    assert tokens == [] or tokens == [""]
"""