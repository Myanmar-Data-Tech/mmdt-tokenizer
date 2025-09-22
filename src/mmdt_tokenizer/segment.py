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
