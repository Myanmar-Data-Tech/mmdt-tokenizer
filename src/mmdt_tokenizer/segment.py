from typing import List


def forward_mm(syllables: List[str], word_dict: set, max_word_len: int) -> List[tuple]:
    """Forward maximum matching segmentation."""
    result, i = [], 0
    while i < len(syllables):
        for j in range(min(max_word_len, len(syllables) - i), 0, -1):
            word = "".join(syllables[i:i + j])
            if word in word_dict:
                result.append((i, i + j, word))
                i += j
                break
        else:
            result.append((i, i + 1, syllables[i]))
            i += 1
    return result


def backward_mm(syllables: List[str], word_dict: set, max_word_len: int) -> List[tuple]:
    """Backward maximum matching segmentation."""
    result, i = [], len(syllables)
    while i > 0:
        for j in range(min(max_word_len, i), 0, -1):
            word = "".join(syllables[i - j:i])
            if word in word_dict:
                result.insert(0, (i - j, i, word))
                i -= j
                break
        else:
            result.insert(0, (i - 1, i, syllables[i - 1]))
            i -= 1
    return result

# -------------------------------
# DAG construction and Viterbi
# -------------------------------
def get_dict_score(dict_weight, word, word_dict: set):
        return dict_weight if word in word_dict else 0.0

def get_bimm_segmentation(syllables, word_dict: set, max_word_len: int) -> list:
    fmm = forward_mm(syllables, word_dict, max_word_len)
    bmm = backward_mm(syllables, word_dict, max_word_len)
    return fmm if len(fmm) <= len(bmm) else bmm
    

def build_dag(syllables: list,max_word_len: int, word_dict: set, use_bimm_fallback:bool) -> dict:
    n = len(syllables)
    dag = {i: [] for i in range(n)}

    # Add dict words + single-syllable fallback (FIXED)
    for i in range(n):
        for j in range(i + 1, min(i + max_word_len + 1, n + 1)):  # +1 to include last index
            word = ''.join(syllables[i:j])
            # Always allow single syllables, even if not in dict (like OppaWord)
            if word in word_dict or j - i == 1:
                dag[i].append((j, word, False))

    # Merge BiMM edges if enabled
    if use_bimm_fallback:
        bimmpath = get_bimm_segmentation(syllables, word_dict, max_word_len)
        for start, end, word in bimmpath:
            dag[start].append((end, word, True))
            
    return dag

# -------------------------------
# Viterbi segmentation
# -------------------------------
def viterbi(syllables: list, dag: dict, bimm_boost: float, word_dict: set, dict_weight: float) -> list:
    """
    DAG + dictionary-based Viterbi segmentation.
    Matches OppaWord (no LM) behavior.
    Scores = dict_weight + syl_score, plus bimm_boost if edge is BiMM
    """
    n = len(syllables)
    scores = [-float('inf')] * (n + 1)
    paths = [None] * (n + 1)
    histories = [[] for _ in range(n + 1)]   
    scores[0] = 0

    for i in range(n):
        for j, word, is_bimm in dag[i]:
            score = get_dict_score(dict_weight, word, word_dict) 
            if is_bimm:
                score += bimm_boost

            if scores[j] < scores[i] + score:
                scores[j] = scores[i] + score
                paths[j] = (i, word)
                histories[j] = histories[i] + [word]

    # --- backtrack ---
    tokens = []
    i = n
    while i > 0:
        if paths[i] is None:
            # fallback in case something goes wrong
            tokens.insert(0, syllables[i-1])
            i -= 1
        else:
            prev_i, word = paths[i]
            tokens.insert(0, word)
            i = prev_i
    return tokens
