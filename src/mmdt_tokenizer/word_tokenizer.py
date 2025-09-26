import pandas as pd
from typing import List, Union, Optional

from .preprocess import preprocess_text, normalize_input
from .postprocess import refine_tokens, split_mixed_tokens
from .segment import forward_mm, backward_mm, build_dag, viterbi
from .csv_utils import save_tokens_to_csv
from .constants import BREAK_PATTERN


class MyanmarWordTokenizer:
    """Word-level tokenizer for Myanmar text."""

    def __init__(self, word_dict: set, space_remove_mode="my_not_num", use_bimm_fallback=True, max_word_len=6,
                 dict_weight: float = 10.0, bimm_boost: float = 150):
        self.word_dict = word_dict
        self.space_remove_mode = space_remove_mode
        self.use_bimm_fallback = use_bimm_fallback
        self.max_word_len = max(3, min(12, max_word_len)) # Fixme: reason for the numbers 3 and 12?
        self.dict_weight: float = dict_weight      # <-- dictionary score : need to investigate why default is 10
        self.bimm_boost: float = bimm_boost        # <-- BiMM score boost : need to investigate why default is 150

    def tokenize(
        self,
        texts: Union[str, List[str], pd.Series, pd.DataFrame],
        return_list=True,
        separator=" ",
        save_csv: Optional[str] = None,
        conll_style=True,
        column: Optional[str] = None,
    ):
        # print(f"Tokenizing input texts...{texts}")
        
        series = normalize_input(texts, column)
        all_tokens = series.apply(self._tokenize_one).tolist()

        if save_csv:
            flat = [tok for sublist in all_tokens for tok in sublist] if len(all_tokens) > 1 else all_tokens[0]
            save_tokens_to_csv(flat, save_csv, conll_style)

        return all_tokens if return_list else [separator.join(toks) for toks in all_tokens]
    
    def _syllable_break(self, text: str) -> list:
        result = BREAK_PATTERN.sub(r'|\1', text)
        if result.startswith('|'):
            result = result[1:]
        return result.split('|')
    
    def _tokenize_one(self, text: str) -> List[str]:
        text = preprocess_text(text, self.space_remove_mode)
        syllables = self._syllable_break(text)
        # Get segmentation using DAG + BiMM fallback
        path = self._choose_segmentation(syllables)
        # Normalize path to token list
        if path and isinstance(path[0], tuple):
            tokens = [w for (_, _, w) in path]
        elif path:
            tokens = path
        else:
            tokens = syllables  # fallback: keep original syllables
        tokens = [t.strip() for t in tokens if t.strip()]
        # Split mixed Burmese+English
        # tokens = split_mixed_tokens(tokens)
        return refine_tokens(tokens)

    def _choose_segmentation(self, syllables: list) -> list:
        dag = build_dag(syllables, self.max_word_len, self.word_dict, self.use_bimm_fallback)

        tokens = viterbi(syllables, dag, self.bimm_boost, self.word_dict, self.dict_weight) if dag else \
                [w for (_, _, w) in forward_mm(syllables, self.word_dict, self.max_word_len)]

        result = []
        i = 0
        for tok in tokens:
            result.append((i, i + len(tok), tok))
            i += len(tok)
        return result
