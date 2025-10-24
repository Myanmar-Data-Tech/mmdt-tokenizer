import pandas as pd
from typing import List, Union, Optional

from ..utils.data_utils import standardize_text_input
from ..utils.csv_utils import save_tokens_to_csv
from .rule_segmenter import rule_segment

from mmdt_tokenizer.preprocessing import preprocess_burmese_text

class MyanmarWordTokenizer:
    """Word-level tokenizer for Myanmar text."""

    def __init__(self, word_dict: set, space_remove_mode="my_not_num", use_bimm_fallback=True, max_word_len=6,
                 dict_weight: float = 10.0, bimm_boost: float = 150, protect_pattern :bool = True):
        self.word_dict = word_dict
        self.space_remove_mode = space_remove_mode
        self.use_bimm_fallback = use_bimm_fallback
        self.max_word_len = max(3, min(12, max_word_len)) # constrain max_word_len to [3, 12]
        self.dict_weight: float = dict_weight      # <-- dictionary score 
        self.bimm_boost: float = bimm_boost        # <-- BiMM score boost
        self.protect_pattern:bool = protect_pattern

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
            flat = [tok for sublist in all_tokens for tok in sublist] if len(all_tokens) > 1 else all_tokens[0]
            save_tokens_to_csv(flat, save_csv, conll_style)

        return all_tokens if return_list else [separator.join(toks) for toks in all_tokens]
    
    def _tokenize_one(self, text: str) -> List[str]:
        if self.protect_pattern:
            phrase_tokens, protected = preprocess_burmese_text(text)     
            final_tokens = []
            for phrase_tok in phrase_tokens:
                if phrase_tok in protected:  # protected span → single token
                    final_tokens.append(protected[phrase_tok])
                else:  # rule-based segmentation
                    segged = rule_segment(phrase_tok)
                    final_tokens.extend(segged)
            return final_tokens
        else: # rule-based segmentation
            final_tokens = rule_segment(text)
            return final_tokens



