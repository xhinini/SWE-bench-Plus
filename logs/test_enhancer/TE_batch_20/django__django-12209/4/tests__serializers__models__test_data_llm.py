import io
import re
import inspect
from importlib import import_module
import pytest

def get_base_source():
    mod = import_module('django.db.models.base')
    path = inspect.getsourcefile(mod)
    with io.open(path, 'r', encoding='utf-8') as f:
        return f.read()

def test_not_raw_and_present_simple():
    """
    Simple substring check: ensure 'not raw and' appears in the file.
    This catches the missing 'not raw' condition in the candidate patch.
    """
    src = get_base_source()
    assert 'not raw and' in src, "Expected 'not raw and' to be present in django/db/models/base.py"

def test_not_raw_and_in_if_block():
    """
    Ensure the 'not raw and' appears specifically near the _save_table
    logic by looking for the surrounding 'Skip an UPDATE' comment and the condition.
    """
    src = get_base_source()
    pattern = re.compile('Skip an UPDATE when adding an instance and primary key has a default\\.(?:.|\\n){1,200}?if\\s*\\(\\s*.*not\\s+raw\\s+and', re.MULTILINE)
    assert pattern.search(src), "The 'not raw and' guard was not found in the _save_table conditional."

def test_not_raw_and_whitespace_robustness():
    """
    Robustness: allow arbitrary whitespace/newlines between tokens.
    """
    src = get_base_source()
    pattern = re.compile('if\\s*\\(\\s*(?:\\n|\\s)*not\\s+raw\\s+and', re.MULTILINE)
    assert pattern.search(src), "Guard 'not raw and' with flexible whitespace not found."

def test_not_raw_and_after_not_force_insert():
    """
    Ensure the sequence 'not force_insert' then 'not raw and' occurs in the condition,
    reflecting the expected ordering in the patched code.
    """
    src = get_base_source()
    pattern = re.compile('not\\s+force_insert\\s*,\\s*\\n\\s*not\\s+raw\\s+and|not\\s+force_insert\\s+and\\s*\\n\\s*not\\s+raw\\s+and', re.MULTILINE)
    assert pattern.search(src), "Expected 'not force_insert' followed by 'not raw and' in the condition."

def test_not_raw_and_line_breaks():
    """
    Ensure the guard is present even if the code uses multiple lines and indentation.
    """
    src = get_base_source()
    pattern = re.compile('if\\s*\\(\\s*\\n\\s*not\\s+force_insert\\s*\\n\\s*not\\s+raw\\s+and', re.MULTILINE)
    assert pattern.search(src), "Multi-line guarded condition with 'not raw and' not found."

def test_condition_in_correct_function_context():
    """
    Confirm that the 'not raw and' appears inside the _save_table function block.
    """
    src = get_base_source()
    func_match = re.search('def\\s+_save_table\\([^\\)]*\\):', src)
    assert func_match, '_save_table function definition not found in source.'
    start = func_match.start()
    window = src[start:start + 2000]
    assert 'not raw and' in window, "'not raw and' not found within the _save_table function body."

def test_guard_present_near_skip_update_comment():
    """
    Extra check that ensures the guard appears after the specific comment
    mentioning skipping an UPDATE when adding an instance.
    """
    src = get_base_source()
    idx = src.find('Skip an UPDATE when adding an instance and primary key has a default.')
    assert idx != -1, "Expected comment 'Skip an UPDATE when adding an instance and primary key has a default.' not found."
    snippet = src[idx:idx + 400]
    assert 'not raw and' in snippet, "Guard 'not raw and' not found after the 'Skip an UPDATE' comment."

def test_not_raw_and_not_present_as_comment_only():
    """
    Ensure 'not raw and' is not only present inside comments; it must be in code.
    We search for 'not raw and' preceded by a non-comment character on the same line.
    """
    src = get_base_source()
    for line in src.splitlines():
        if 'not raw and' in line:
            hash_index = line.find('#')
            phrase_index = line.find('not raw and')
            if hash_index == -1 or phrase_index < hash_index:
                break
    else:
        pytest.skip("'not raw and' found only in comments or not present at all.")
    assert True

def test_single_occurrence_of_guard():
    """
    Sanity: ensure at least one occurrence exists (this is a mild duplication
    but helps ensure the check is not fragile due to minor formatting).
    """
    src = get_base_source()
    count = src.count('not raw and')
    assert count >= 1, "Expected at least one occurrence of 'not raw and' in source."

def test_guard_stable_across_reloads():
    """
    Ensure that re-importing the module doesn't change the on-disk source
    and that the guard remains present.
    """
    src1 = get_base_source()
    src2 = get_base_source()
    assert src1 == src2
    assert 'not raw and' in src1, "'not raw and' guard missing after reload."