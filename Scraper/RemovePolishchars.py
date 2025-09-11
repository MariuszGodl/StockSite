from Other.imports import *

POLISH_MAP = str.maketrans({
    "Ą": "A", "ą": "a",
    "Ć": "C", "ć": "c",
    "Ę": "E", "ę": "e",
    "Ł": "L", "ł": "l",
    "Ń": "N", "ń": "n",
    "Ó": "O", "ó": "o",
    "Ś": "S", "ś": "s",
    "Ź": "Z", "ź": "z",
    "Ż": "Z", "ż": "z",
})

def strip_polish_chars(text: str) -> str:
    if text is None:
        return None
    # Normalize to split combined diacritics
    normalized = unicodedata.normalize("NFD", text)
    # Remove combining marks
    without_marks = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
    # Apply Polish-specific replacements
    return without_marks.translate(POLISH_MAP)