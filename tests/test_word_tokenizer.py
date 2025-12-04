import pytest
from mmdt_tokenizer import MyanmarTokenizer

@pytest.fixture(scope="module")
def tokenizer():
    return MyanmarTokenizer()


def test_conjunctions(tokenizer):
    text = "အဲဒီအချိန်ကတည်းကစက်ရုံကို စွန့်ခွာသွားတာဖြစ်ပါတယ်။ကြိုးစားသော်လည်း စာမေးပွဲကျပါသည်။သို့သော် စိတ်မပျက်ပါ။"
    tokens = tokenizer.word_tokenize(text)
    expected = [['အဲဒီအချိန်', 'ကတည်းက', 'စက်ရုံ', 'ကို', 'စွန့်ခွာ', 'သွားတာဖြစ်ပါတယ်', '။', 'ကြိုးစား', 'သော်လည်း', 'စာမေးပွဲကျ', 'ပါသည်', '။', 'သို့သော်', 'စိတ်', 'မပျက်ပါ', '။']]
    assert tokens == expected


def test_month_and_date(tokenizer):
    text = "၂၀၂၅ ခုနှစ် မေလ ၅ရက် သည် ကျွန်မတို့အတွက် အရေးပါသည်"
    tokens = tokenizer.word_tokenize(text)
    expected = ['၂၀၂၅ ခုနှစ် မေလ ၅ရက်', 'သည်', 'ကျွန်မတို့', 'အတွက်', 'အရေး', 'ပါသည်']
    assert tokens[0] == expected


def test_negation(tokenizer):
    text = "အစီအစဥ်ကို သူမ စိတ်ဆိုး မနေပါဘူး"
    tokens = tokenizer.word_tokenize(text)
    expected = ['အစီအစဥ်', 'ကို', 'သူမ', 'စိတ်ဆိုး', 'မနေပါဘူး']
    assert tokens[0] == expected

def test_punctuation_only(tokenizer):
    text = "။၊?"
    tokens = tokenizer.word_tokenize(text)
    expected = [[]]
    assert tokens == expected