import pytest
from mmdt_tokenizer import MyanmarTokenizer

@pytest.fixture(scope="module")
def tokenizer():
    return MyanmarTokenizer()

def test_basic_sentence(tokenizer):
    text = "ဒီဆိပ်ကမ်းကို ဇူလိုင် ၁၁ ရက်ကတည်းက ပိတ်ထားတာဖြစ်ပြီး၊ ကျွန်တော်တို့က မသွားနိုင်ဘူး။"
    tokens = tokenizer.word_tokenize(text)
    expected = [['ဒီဆိပ်ကမ်း', 'ကို', 'ဇူလိုင်', '၁၁', 'ရက်', 'က', 'တည်း', 'က', 'ပိတ်ထားတာ', 'ဖြစ်ပြီး', '၊', "ကျွန်တော်", "တို့", 'က', 'မသွားနိုင်ဘူး', '။']]
    assert tokens == expected, f"Got {tokens}"

def test_conjunctions(tokenizer):
    text = "သူသွားမယ် သို့မဟုတ် သူလာမယ်။"
    tokens = tokenizer.word_tokenize(text)
    expected = [["သူသွားမယ်", "သို့မဟုတ်", "သူလာမယ်", "။"]]
    assert tokens == expected

def test_particle_variants(tokenizer):
    text = "သူက ကောင်းတဲ့လူပါ။"
    tokens = tokenizer.word_tokenize(text)
    
    expected = ["သူ", "က", "ကောင်းတဲ့လူပါ", "။"]
    assert tokens[0] == expected

def test_month_and_date(tokenizer):
    text = "မေလ ၁ ရက်နေ့မှာ စတင်မည်။"
    tokens = tokenizer.word_tokenize(text)
    expected = ['မေ', 'လ', '၁', 'ရက်နေ့', 'မှာ', 'စတင်မည်', '။']
    assert tokens[0] == expected


def test_negation(tokenizer):
    text = "ကျွန်မ မသွားဘူး။" #FIXED ME -- FAIL due to the pronoun
    tokens = tokenizer.word_tokenize(text)
    expected = ["ကျွန်မ", "မသွားဘူး", "။"]
    assert tokens[0] == expected

def test_punctuation_only(tokenizer):
    text = "။၊?"
    tokens = tokenizer.word_tokenize(text)
    expected = ["။", "၊", "?"]
    assert tokens[0] == expected