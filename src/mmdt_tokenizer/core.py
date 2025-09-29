from pathlib import Path
from .constants import DICT_FILE_PATH
from .word_tokenizer import MyanmarWordTokenizer
from .syllable_tokenizer import MyanmarSyllableTokenizer


class MyanmarTokenizer:
    """Facade that unifies word-level and syllable-level tokenizers."""

    def __init__(
        self,
        dict_path="../data/myg2p_mypos.dict",
        space_remove_mode="my_not_num",
        use_bimm_fallback=True,
        max_word_len=6,
        dict_weight: float = 10.0,       # <-- dictionary score, review the values later
        bimm_boost: float = 150,        # <-- BiMM score boost, review the values later
        protect_pattern :bool = True    
    ):
        if not Path(dict_path).is_file():
            dict_path = DICT_FILE_PATH
        
        self.dict_path = dict_path
        word_dict = {line.strip() for line in open(self.dict_path, encoding="utf-8") if line.strip()}
        print(f"Loaded {len(word_dict)} words from {self.dict_path}")

        self.word_tokenizer = MyanmarWordTokenizer(
            word_dict=word_dict,
            space_remove_mode=space_remove_mode,
            use_bimm_fallback=use_bimm_fallback,
            max_word_len=max_word_len, 
            dict_weight=dict_weight,
            bimm_boost=bimm_boost,
            protect_pattern=protect_pattern
        )
        self.syllable_tokenizer = MyanmarSyllableTokenizer()

    def word_tokenize(self,*args, **kwargs):
        return self.word_tokenizer.tokenize(*args, **kwargs)

    def syllable_tokenize(self, *args, **kwargs):
        return self.syllable_tokenizer.tokenize(*args, **kwargs)