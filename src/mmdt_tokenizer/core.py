from pathlib import Path
from .tokenizer.word_tokenizer import MyanmarWordTokenizer
from .tokenizer.syllable_tokenizer import MyanmarSyllableTokenizer


class MyanmarTokenizer:
    """Facade that unifies word-level and syllable-level tokenizers."""

    def __init__(
        self,
        protect_pattern :bool = True    # <-- default, it is protected. 
    ):

        # Initialize word tokenizer
        self.word_tokenizer = MyanmarWordTokenizer(protect_pattern=protect_pattern)
        
        # Initialize syllabus tokenizer
        self.syllable_tokenizer = MyanmarSyllableTokenizer()

    
    def word_tokenize(self,*args, **kwargs):
        return self.word_tokenizer.tokenize(*args, **kwargs)

    def syllable_tokenize(self, *args, **kwargs):
        return self.syllable_tokenizer.tokenize(*args, **kwargs)