def _int_to_letters(n: int) -> str:
    """Convert integer to letters for placeholders (A, B, ..., AA, AB, ...)."""
    chars = []
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        chars.append(chr(ord('A') + remainder))
    return "".join(reversed(chars))
