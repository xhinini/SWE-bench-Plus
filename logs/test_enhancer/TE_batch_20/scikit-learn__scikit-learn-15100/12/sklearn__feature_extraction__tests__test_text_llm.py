import pytest
from sklearn.feature_extraction.text import strip_accents_unicode
SAMPLES = [_MyStr('abc'), _MyStr(''), _MyStr('Hello, world!'), _MyStr('12345'), _MyStr("!@#$%^&*()_+-=[];':,./<>?"), _MyStr(' \t\n'), _MyStr('~`'), _MyStr('a' * 1000), _MyStr('The quick brown fox 123'), _MyStr('COOL')]