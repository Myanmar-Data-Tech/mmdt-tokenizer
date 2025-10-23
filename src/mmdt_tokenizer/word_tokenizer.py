import pandas as pd
from typing import List, Union, Optional

from .data_utils import standardize_text_input
from .csv_utils import save_tokens_to_csv
from mmdt_tokenizer.preprocessing import preprocess_burmese_text

from .rule_segmenter import rule_segment

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
                print(phrase_tok)
                if phrase_tok in protected:  # protected span → single token
                    final_tokens.append(protected[phrase_tok])
                else:  # normal segmentation
                    segged = rule_segment(phrase_tok)
                    final_tokens.extend(segged)
            return final_tokens
        else:
            segged = rule_segment(text)
            final_tokens = list(segged.keys())
            return final_tokens


    """
    def _segment_and_refine(self, text: str) -> List[str]:
        #syllables = self._syllable_break(text)
        return list(text)
        
        # Get segmentation using DAG + BiMM fallback
        dag = build_dag(syllables, self.max_word_len, self.word_dict, self.use_bimm_fallback)
        tokens = (
            viterbi(syllables, dag, self.bimm_boost, self.word_dict, self.dict_weight)
            if dag
            else [w for (_, _, w) in forward_mm(syllables, self.word_dict, self.max_word_len)]
        )
        
        # Normalize to tokens
        if tokens and isinstance(tokens[0], tuple):
            tokens = [w for (_, _, w) in tokens]

        tokens = [t.strip() for t in tokens if t.strip()]
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

    def _syllable_break(self, text: str) -> list:
        result = BREAK_PATTERN.sub(r'|\1', text)
        if result.startswith('|'):
            result = result[1:]
        return result.split('|')
    """
