import pytest
from mmdt_tokenizer import MyanmarTokenizer

@pytest.fixture(scope="module")
def tokenizer():
    return MyanmarTokenizer()


def test_conjunctions(tokenizer):
    text = "သူသွားမယ်သို့မဟုတ်သူလာမယ်။"
    tokens = tokenizer.word_tokenize(text)
    expected = [["သူ", "သွားမယ်", "သို့မဟုတ်", "သူ", "လာမယ်။"]]
    assert tokens == expected


def test_month_and_date(tokenizer):
    text = "မေလ ၁ ရက်နေ့မှာ စတင်မည်။"
    tokens = tokenizer.word_tokenize(text)
    expected = ['မေလ', '၁ရက်နေ့မှာ', "စတင်", "မည်။"]
    assert tokens[0] == expected


def test_negation(tokenizer):
    text = "အစီအစဥ်ကို သူမစိတ်ဆိုး မနေပါဘူး"
    tokens = tokenizer.word_tokenize(text)
    expected = ['အစီအစဥ်ကို', 'သူမစိတ်ဆိုး', 'မနေပါဘူး']
    assert tokens[0] == expected

def test_punctuation_only(tokenizer):
    text = "။၊?"
    tokens = tokenizer.word_tokenize(text)
    expected = [[]]
    assert tokens == expected