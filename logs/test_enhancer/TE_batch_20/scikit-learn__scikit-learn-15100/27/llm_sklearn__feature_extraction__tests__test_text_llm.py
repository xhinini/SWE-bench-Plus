import unicodedata
import unicodedata
import pytest
from sklearn.feature_extraction.text import strip_accents_unicode
ASCII_STRINGS = ['hello world', 'The quick brown fox jumps over the lazy dog.', '', "12345 !@#$$%^&*()_+-=[]{};':,./<>?", 'A' * 2000]
NONASCII_STRINGS = ['àáâãäåçèéêë', 'إ', 'ö', '̀́̂̃', 'mañana']