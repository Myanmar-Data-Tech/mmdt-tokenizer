import pandas as pd
from typing import List, Union, Optional

from ..utils.data_utils import standardize_text_input
from ..utils.csv_utils import save_tokens_to_csv
from ..rule_segmenter.engine import rule_segment
from ..preprocessing import preprocess_burmese_text
from .syllable_tokenizer import MyanmarSyllableTokenizer

def get_syllabus_from_tokenizer(tokenizer: MyanmarSyllableTokenizer):
    """Adapter: returns callable get_syllabus(text) -> List[str]."""
    def get_syllabus(text: str) -> List[str]:
        lists = tokenizer.tokenize(text, return_list=True)
        if not lists:
            return []
        return lists[0] if isinstance(lists[0], list) else lists
    return get_syllabus

class MyanmarWordTokenizer:
    """Word-level tokenizer using syllable segmentation + rule-based segmentation."""

    def __init__(self, protect_pattern :bool = True):
        
        self.protect_pattern:bool = protect_pattern
        self.syllable_tokenizer = MyanmarSyllableTokenizer()
        self._get_syllabus = get_syllabus_from_tokenizer(self.syllable_tokenizer)

    def tokenize(
        self,
        texts: Union[str, List[str], pd.Series, pd.DataFrame],
        return_list=True,
        separator=" ",
        save_csv: Optional[str] = None,
        conll_style=True,
        column: Optional[str] = None,
    ):
        
        series = standardize_text_input(texts, column)
        all_tokens = series.apply(self._tokenize_one).tolist()

        if save_csv:
            save_tokens_to_csv(all_tokens, save_csv, conll_style)

        return all_tokens if return_list else [separator.join(toks) for toks in all_tokens]
    
    def _tokenize_one(self, text: str) -> List[str]:
        if self.protect_pattern:
            phrase_tokens, protected = preprocess_burmese_text(text)     
            final_tokens = []
            for phrase_tok in phrase_tokens:
                if phrase_tok in protected:  # protected span → single token
                    final_tokens.append(protected[phrase_tok])
                else:  # rule-based segmentation
                    segged = rule_segment(phrase_tok, get_syllabus=self._get_syllabus)
                    final_tokens.extend(segged)
            return final_tokens
        else: # rule-based segmentation
            final_tokens = rule_segment(text, get_syllabus=self._get_syllabus)
            return final_tokens



