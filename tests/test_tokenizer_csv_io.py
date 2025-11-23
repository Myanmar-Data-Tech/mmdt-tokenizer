# tests/test_tokenizer_csv_io.py
import pandas as pd
from pathlib import Path
import pytest

from mmdt_tokenizer import MyanmarTokenizer
from mmdt_tokenizer.tokenizer.syllable_tokenizer import MyanmarSyllableTokenizer
from mmdt_tokenizer.utils.config import DATA_DIR, OUTPUT_DIR


@pytest.fixture(scope="module")
def tokenizer():
    return MyanmarTokenizer()

@pytest.fixture(scope="module")
def syllable_tokenizer():
    return MyanmarSyllableTokenizer()


def test_syllable_tokenize_csv(syllable_tokenizer):
    """Test CSV loading/saving for syllable tokenizer."""
    csv_input_path = DATA_DIR / "test_data.csv"
    csv_output_path = OUTPUT_DIR / "result_syllable_bd.csv"

    # Sample input DataFrame for testing
    df = pd.read_csv(csv_input_path)

    syllable_tokenizer.tokenize(
        df,
        column="original_sentence",
        save_csv=str(csv_output_path),
        conll_style=False,
    )
    print(csv_output_path)
    assert Path(csv_output_path).exists(), "Output CSV not created."


def test_word_tokenize_csv(tokenizer):
    """Test CSV loading/saving for word tokenizer."""
    csv_input_path = DATA_DIR / "test_data.csv"
    csv_output_path = OUTPUT_DIR / "result_word_bd.csv"

    df = pd.read_csv(csv_input_path)

    tokenizer.word_tokenize(
        df,
        column="original_sentence",
        save_csv=str(csv_output_path),
        conll_style=False,
    )

    assert Path(csv_output_path).exists(), "Output CSV not created."


def test_word_tokenize_conll_style(tokenizer):
    """Test word tokenizer with CoNLL-style CSV output (vertical format)."""
    csv_input_path = DATA_DIR / "test_data.csv"
    csv_output_path = OUTPUT_DIR / "result_word_conll.csv"

    df = pd.read_csv(csv_input_path)

    tokenizer.word_tokenize(
        df,
        column="original_sentence",
        save_csv=str(csv_output_path),
        conll_style=True,
    )

    assert Path(csv_output_path).exists(), "CoNLL output CSV not created."

    df_out = pd.read_csv(csv_output_path)
    assert df_out.shape[1] in (1, 2), "Unexpected number of columns in CoNLL-style CSV"


def test_tagging_csv(tokenizer):
    """Tests the CSV loading/saving feature exposed by the main tokenizer."""
    csv_input_path = DATA_DIR /"test_data.csv" 
    csv_text_path = OUTPUT_DIR / "result_word_text.csv"
    csv_output_path = OUTPUT_DIR / "result_word_tag.csv"

    df = pd.read_csv(csv_input_path)
    
    tokenizer.word_tokenize(df,column = 'original_sentence', 
                                     save_csv=str(csv_text_path), save_tag=str(csv_output_path), 
                                     conll_style=False)

    assert Path(csv_output_path).exists()