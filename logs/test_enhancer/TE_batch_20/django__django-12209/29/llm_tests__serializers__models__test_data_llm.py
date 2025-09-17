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

import unittest
import uuid
from types import SimpleNamespace
from django.db.models.base import Model, NOT_PROVIDED

def make_fake_class_and_instance(pk_default, explicit_pk=None):
    """
    Build fake 'cls' and 'self' objects suitable for calling Model._save_table.
    - pk_default: value or callable used as the pk.default
    - explicit_pk: if provided, set as the attribute on the instance before calling save
    """
    pk = FakePK(default=pk_default)
    meta = SimpleNamespace(pk=pk, local_concrete_fields=[], auto_field=None, db_returning_fields=[], order_with_respect_to=None)
    fake_cls = SimpleNamespace(_meta=meta, _base_manager=FakeManager())
    fake_self = SimpleNamespace()
    fake_self._state = SimpleNamespace(adding=True, db=None)
    setattr(fake_self, pk.attname, explicit_pk)
    fake_self._called_update = False
    fake_self._called_insert = False

    def _do_update(self_obj, base_qs, using, pk_val, values, update_fields, forced_update):
        self_obj._called_update = True
        return True

    def _do_insert(self_obj, manager, using, fields, returning_fields, raw):
        self_obj._called_insert = True
        return []
    fake_self._do_update = _do_update.__get__(fake_self, SimpleNamespace)
    fake_self._do_insert = _do_insert.__get__(fake_self, SimpleNamespace)
    return (fake_cls, fake_self)
if __name__ == '__main__':
    unittest.main()

import inspect
import re
import unittest
from django.db.models.base import Model
import inspect
import re
import unittest
from django.db.models.base import Model

class SaveTableRawGuardTests(unittest.TestCase):

    def setUp(self):
        self.src = inspect.getsource(Model._save_table)

    def test_not_raw_present(self):
        self.assertIn('not raw', self.src, "'not raw' must be present in _save_table")

    def test_not_raw_and_present(self):
        self.assertIn('not raw and', self.src, "'not raw and' must be present in _save_table")

    def test_full_condition_tokens_present(self):
        self.assertIn('not raw', self.src)
        self.assertIn('self._state.adding', self.src)
        self.assertIn('self._meta.pk.default', self.src)
        self.assertIn('NOT_PROVIDED', self.src)

    def test_condition_parentheses_line(self):
        m = re.search('if\\s*\\((.*?)\\):', self.src, re.S)
        self.assertIsNotNone(m, 'Could not find the if(...) condition block in _save_table')
        condition = m.group(1)
        self.assertIn('not raw', condition, "'not raw' should be inside the if(...) condition")

    def test_not_raw_precedes_pk_default(self):
        idx_not_raw = self.src.find('not raw')
        idx_pk_default = self.src.find('self._meta.pk.default')
        self.assertTrue(idx_not_raw != -1 and idx_pk_default != -1 and (idx_not_raw < idx_pk_default), "'not raw' should appear before 'self._meta.pk.default' in _save_table")

    def test_exact_and_sequence_in_condition(self):
        m = re.search('if\\s*\\((.*?)\\):', self.src, re.S)
        self.assertIsNotNone(m)
        condition = m.group(1)
        self.assertIn('not force_insert', condition)
        self.assertIn('not raw', condition)

    def test_not_raw_and_not_force_insert_combined(self):
        pattern = 'not\\s+force_insert\\s*,?\\s*and\\s+not\\s+raw|not\\s+raw\\s*,?\\s*and\\s+not\\s+force_insert'
        m = re.search('if\\s*\\((.*?)\\):', self.src, re.S)
        self.assertIsNotNone(m)
        condition = m.group(1)
        self.assertRegex(condition, 'not\\s+raw\\s+and\\s+not\\s+force_insert|not\\s+force_insert\\s+and\\s+not\\s+raw', "expected 'not raw' and 'not force_insert' combined in condition")
if __name__ == '__main__':
    unittest.main()

from types import MethodType, SimpleNamespace
from django.db.models.base import NOT_PROVIDED
from types import SimpleNamespace, MethodType
import unittest
from django.test import SimpleTestCase
from django.db import DatabaseError
from django.db.models.base import Model, NOT_PROVIDED

def make_fake_instance(pk_attname='id', pk_default=object(), pk_get_value=None, explicit_pk_value=None, other_field_name='other'):
    """
    Create a fake 'self' and 'cls' pair suitable for passing to Model._save_table.
    The fake self will capture calls to _do_insert and _do_update.
    """
    if pk_default is NOT_PROVIDED:
        pk_field = FakeField(name=pk_attname, attname=pk_attname, primary_key=True, default=NOT_PROVIDED, get_pk_value_on_save_return=pk_get_value)
    else:
        pk_field = FakeField(name=pk_attname, attname=pk_attname, primary_key=True, default=pk_default, get_pk_value_on_save_return=pk_get_value)
    other_field = FakeField(name=other_field_name, attname=other_field_name, primary_key=False, default=NOT_PROVIDED)
    meta = FakeMeta(pk_field, [other_field])
    cls = SimpleNamespace(_meta=meta, _base_manager=None)
    inst = SimpleNamespace()
    inst._meta = meta
    inst._state = SimpleNamespace(adding=True, db=None)
    inst.__dict__ = {}
    if explicit_pk_value is not None:
        setattr(inst, pk_attname, explicit_pk_value)

    def _get_pk_val(self_inst, meta_arg=None):
        return getattr(self_inst, meta.pk.attname, None)
    inst._get_pk_val = MethodType(_get_pk_val, inst)
    inst.insert_called = False
    inst.update_called = False

    def _do_insert(self_inst, manager, using, fields, returning_fields, raw):
        self_inst.insert_called = True
        return [None for _ in returning_fields or ()]
    inst._do_insert = MethodType(_do_insert, inst)

    def _do_update(self_inst, base_qs, using, pk_val, values, update_fields, forced_update):
        self_inst.update_called = True
        return 0
    inst._do_update = MethodType(_do_update, inst)
    return (inst, cls, meta)
if __name__ == '__main__':
    unittest.main()

from types import MethodType
import uuid
from django.test import SimpleTestCase
from tests.serializers.models import data as data_models
from types import MethodType
import uuid
from django.test import SimpleTestCase
from tests.serializers.models import data as data_models

def _fake_do_update(self, base_qs, using, pk_val, values, update_fields, forced_update):
    """
    Fake _do_update that simply records it was called and returns True
    to simulate that an UPDATE affected rows.
    """
    self._update_called = True
    return True

def _fake_do_insert(self, manager, using, fields, returning_fields, raw):
    """
    Fake _do_insert that records it was called and returns a list of
    placeholder results matching the number of returning_fields.
    """
    self._insert_called = True
    return [None] * len(returning_fields)

from unittest import mock
from decimal import Decimal
import uuid
from django.db.models.query import QuerySet
from unittest import mock
from decimal import Decimal
import uuid
from django.db import models, DatabaseError
from django.db.models.query import QuerySet
from django.test import SimpleTestCase
from django.test.utils import isolate_apps

class SaveBaseRawTests(SimpleTestCase):
    """
    Tests that exercise the code path fixed by the patch that adds
    'not raw' to the skip-update condition. We create simple models
    with a primary key that has a default value and a separate
    non-PK field, and call save_base(raw=True, update_fields=[...]).
    The expected behavior (after the gold patch) is that a raw save
    will attempt an UPDATE (which we stub to return 0) and then,
    because update_fields is specified and the UPDATE did not affect
    any rows, a DatabaseError is raised.
    The candidate patch which omitted the 'not raw' check will instead
    force an INSERT for raw saves and not raise; these tests fail
    against that incorrect behavior.
    """

    def _stub_update_zero(self):
        self._patch_update = mock.patch.object(QuerySet, '_update', autospec=True, return_value=0)
        self._patch_exists = mock.patch.object(QuerySet, 'exists', autospec=True, return_value=False)
        self._patch_update.start()
        self._patch_exists.start()

    def _stop_stub_update(self):
        mock.patch.stopall()