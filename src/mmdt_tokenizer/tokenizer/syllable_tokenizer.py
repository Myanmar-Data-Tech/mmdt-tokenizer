import pandas as pd
from typing import List, Union, Optional

from ..utils.data_utils import standardize_text_input
from ..utils.csv_utils import save_tokens_to_csv
from ..utils.patterns import SYLLABLE_BREAK_PATTERN


class MyanmarSyllableTokenizer:
    """Syllable-level tokenizer for Myanmar text."""

    def __init__(self, separator=" "):
        self.separator = separator

    def tokenize(
        self,
        texts: Union[str, List[str], pd.Series, pd.DataFrame],
        return_list=True,
        save_csv: Optional[str] = None,
        conll_style=True,
        column: Optional[str] = None,
    ):
        series = standardize_text_input(texts, column)
        all_syllables = series.apply(self._break_one).tolist()
        if save_csv:
            save_tokens_to_csv(all_syllables, save_csv, conll_style)

        return all_syllables if return_list else [self.separator.join(syls) for syls in all_syllables]

    def _break_one(self, text: str) -> List[str]:
        segmented = SYLLABLE_BREAK_PATTERN.sub(self.separator + r"\1", text.strip())
        tokens = segmented.lstrip(self.separator).split(self.separator)
        cleaned_tokens = [tok for tok in tokens if tok] 
        return cleaned_tokens
