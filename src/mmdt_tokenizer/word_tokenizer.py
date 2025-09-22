import pandas as pd
from typing import List, Union, Optional

from .preprocess import preprocess_text, normalize_input
from .postprocess import refine_tokens
from .segment import forward_mm, backward_mm
from .csv_utils import save_tokens_to_csv


class MyanmarWordTokenizer:
    """Word-level tokenizer for Myanmar text."""

    def __init__(self, word_dict: set, space_remove_mode="my_not_num", use_bimm_fallback=True, max_word_len=6):
        self.word_dict = word_dict
        self.space_remove_mode = space_remove_mode
        self.use_bimm_fallback = use_bimm_fallback
        self.max_word_len = max(3, min(12, max_word_len)) # Fixme: reason for the numbers 3 and 12?

    def tokenize(
        self,
        texts: Union[str, List[str], pd.Series, pd.DataFrame],
        return_list=True,
        separator=" ",
        save_csv: Optional[str] = None,
        conll_style=True,
        column: Optional[str] = None,
    ):
        print(f"Tokenizing input texts...{texts}")
        
        series = normalize_input(texts, column)
        all_tokens = series.apply(self._tokenize_one).tolist()

        if save_csv:
            flat = [tok for sublist in all_tokens for tok in sublist] if len(all_tokens) > 1 else all_tokens[0]
            save_tokens_to_csv(flat, save_csv, conll_style)

        return all_tokens if return_list else [separator.join(toks) for toks in all_tokens]
    
    def _tokenize_one(self, text: str) -> List[str]:
        text = preprocess_text(text, self.space_remove_mode)
        syllables = list(text)  # assume syllable_break already applied
        path = self._choose_segmentation(syllables)
        tokens = [w for (_, _, w) in path]
        return refine_tokens(tokens)

    def _choose_segmentation(self, syllables: List[str]):
        fmm = forward_mm(syllables, self.word_dict, self.max_word_len)
        if not self.use_bimm_fallback:
            return fmm
        bmm = backward_mm(syllables, self.word_dict, self.max_word_len)
        return fmm if len(fmm) <= len(bmm) else bmm