def test_only_relation_agnostic_fields_handles_missing_to_key_single_field(self):
    """only_relation_agnostic_fields must not KeyError if deconstruct omits 'to'."""

    class HardNoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    fk = HardNoToFK('testapp.Author', on_delete=models.CASCADE)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    result = autodetector.only_relation_agnostic_fields({'fk': fk})
    self.assertIsInstance(result, list)
    for deconstructed in result:
        self.assertNotIn('to', deconstructed[2])

def test_only_relation_agnostic_fields_handles_missing_to_key_multiple_fields(self):
    """Multiple fields including one with missing 'to' must be handled fine."""

    class HardNoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    fk = HardNoToFK('testapp.Author', on_delete=models.CASCADE)
    char = models.CharField(max_length=10)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    result = autodetector.only_relation_agnostic_fields({'b': char, 'a': fk})
    self.assertEqual(len(result), 2)
    fk_decs = [d for d in result if isinstance(d, tuple) and (d[0] == 'django.db.models.ForeignKey' or 'ForeignKey' in str(d[0]))]
    for d in fk_decs:
        self.assertNotIn('to', d[2])

def test_create_model_with_missing_to_fk_does_not_error(self):
    """Creating a model with a FK whose deconstruct omits 'to' should succeed."""

    class HardNoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    book = ModelState('testapp', 'Book', [('id', models.AutoField(primary_key=True)), ('author', HardNoToFK('testapp.Author', on_delete=models.CASCADE))])
    author = ModelState('testapp', 'Author', [('id', models.AutoField(primary_key=True))])
    changes = self.get_changes([], [author, book])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel', 'CreateModel'])

def test_delete_model_with_missing_to_fk_does_not_error(self):
    """Deleting a model that contains a FK with missing 'to' must not error."""

    class HardNoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    book = ModelState('testapp', 'Book', [('id', models.AutoField(primary_key=True)), ('author', HardNoToFK('testapp.Author', on_delete=models.CASCADE))])
    author = ModelState('testapp', 'Author', [('id', models.AutoField(primary_key=True))])
    changes = self.get_changes([author, book], [author])
    self.assertNumberMigrations(changes, 'testapp', 1)
    types = [op.__class__.__name__ for op in changes['testapp'][0].operations]
    self.assertIn('DeleteModel', types)

def test_detect_rename_model_with_missing_to_on_new(self):
    """generate_renamed_models must handle new model having FK deconstruct that omits 'to'."""

    class HardNoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    old = ModelState('app', 'Old', [('id', models.AutoField(primary_key=True)), ('ref', models.IntegerField())])
    new = ModelState('app', 'New', [('id', models.AutoField(primary_key=True)), ('ref', HardNoToFK('app.Target', on_delete=models.CASCADE))])
    changes = self.get_changes([old], [new], MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    ops = [op.__class__.__name__ for op in changes['app'][0].operations]
    self.assertTrue('RenameModel' in ops or 'CreateModel' in ops)

def test_detect_rename_model_with_missing_to_on_old(self):
    """generate_renamed_models must handle old model having FK deconstruct that omits 'to'."""

    class HardNoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    old = ModelState('app', 'Old', [('id', models.AutoField(primary_key=True)), ('ref', HardNoToFK('app.Target', on_delete=models.CASCADE))])
    new = ModelState('app', 'New', [('id', models.AutoField(primary_key=True)), ('ref', models.ForeignKey('app.Target', on_delete=models.CASCADE))])
    changes = self.get_changes([old], [new], MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    ops = [op.__class__.__name__ for op in changes['app'][0].operations]
    self.assertTrue('RenameModel' in ops or 'CreateModel' in ops)

def test_multiple_fk_fields_with_one_missing_to_does_not_error(self):
    """Mixed fields where one FK deconstruct omits 'to' must not raise."""

    class HardNoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    state_before = []
    state_after = [ModelState('app', 'A', [('id', models.AutoField(primary_key=True)), ('fk1', HardNoToFK('app.T1', on_delete=models.CASCADE)), ('fk2', models.ForeignKey('app.T2', on_delete=models.CASCADE))]), ModelState('app', 'T1', [('id', models.AutoField(primary_key=True))]), ModelState('app', 'T2', [('id', models.AutoField(primary_key=True))])]
    changes = self.get_changes(state_before, state_after)
    self.assertNumberMigrations(changes, 'app', 1)
    types = [op.__class__.__name__ for op in changes['app'][0].operations]
    self.assertIn('CreateModel', types)

def test_only_relation_agnostic_fields_omits_to_for_normal_fk(self):
    """For a regular ForeignKey, only_relation_agnostic_fields should remove 'to'."""
    fk = models.ForeignKey('testapp.Author', on_delete=models.CASCADE)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    result = autodetector.only_relation_agnostic_fields({'fk': fk})
    for deconstructed in result:
        self.assertNotIn('to', deconstructed[2])

def test_deep_deconstruct_with_empty_kwargs_and_missing_to(self):
    """deep_deconstruct + only_relation_agnostic_fields must handle deconstruct returning empty kwargs."""

    class NoKwargsFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            return (name, path, args, {})
    fk = NoKwargsFK('testapp.Author', on_delete=models.CASCADE)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    result = autodetector.only_relation_agnostic_fields({'f': fk})
    self.assertEqual(len(result), 1)
    self.assertNotIn('to', result[0][2])

def test_rename_model_with_hardcoded_fk_missing_to(self):
    """
    A model rename where the foreign key deconstruct() omits 'to' should
    not raise and should detect the rename.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('testapp', 'OldAuthor', [('id', models.AutoField(primary_key=True)), ('ref', HardcodedForeignKey(on_delete=models.CASCADE))])]
    after = [ModelState('testapp', 'NewAuthor', [('id', models.AutoField(primary_key=True)), ('ref', HardcodedForeignKey(on_delete=models.CASCADE))])]
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])

def test_rename_model_old_normal_new_hardcoded_fk(self):
    """
    Old model uses a normal FK deconstructing with 'to', new model uses a
    custom FK that omits 'to'. Should detect the rename without error.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('testapp', 'OldAuthor', [('id', models.AutoField(primary_key=True)), ('ref', models.ForeignKey('testapp.Author', models.CASCADE))])]
    after = [ModelState('testapp', 'NewAuthor', [('id', models.AutoField(primary_key=True)), ('ref', HardcodedForeignKey(on_delete=models.CASCADE))])]
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])

def test_rename_model_old_hardcoded_new_normal_fk(self):
    """
    Old model uses a custom FK omitting 'to', new model uses normal FK. Should
    detect the rename without error.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('testapp', 'OldAuthor', [('id', models.AutoField(primary_key=True)), ('ref', HardcodedForeignKey(on_delete=models.CASCADE))])]
    after = [ModelState('testapp', 'NewAuthor', [('id', models.AutoField(primary_key=True)), ('ref', models.ForeignKey('testapp.Author', models.CASCADE))])]
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])

def test_rename_field_with_hardcoded_fk_missing_to(self):
    """
    Field rename where the FK deconstruct() omits 'to' should not raise
    and should detect the RenameField.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('app', 'Thing', [('id', models.AutoField(primary_key=True)), ('oldname', HardcodedForeignKey(on_delete=models.CASCADE))])]
    after = [ModelState('app', 'Thing', [('id', models.AutoField(primary_key=True)), ('newname', HardcodedForeignKey(on_delete=models.CASCADE))])]
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameField'])

def test_only_relation_agnostic_fields_handles_missing_to_direct(self):
    """
    Directly calling only_relation_agnostic_fields with a field whose
    deconstruct() omits 'to' should not raise and should return a list.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'ref': HardcodedForeignKey(on_delete=models.CASCADE)}
    result = autodetector.only_relation_agnostic_fields(fields)
    self.assertIsInstance(result, list)
    self.assertGreaterEqual(len(result), 1)

def test_rename_model_with_multiple_fks_some_missing_to(self):
    """
    Model rename when a model has multiple ForeignKeys, some of which
    deconstruct() without 'to', must not raise and must detect the rename.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('testapp', 'OldThing', [('id', models.AutoField(primary_key=True)), ('a', HardcodedForeignKey(on_delete=models.CASCADE)), ('b', models.ForeignKey('testapp.Author', models.CASCADE))])]
    after = [ModelState('testapp', 'NewThing', [('id', models.AutoField(primary_key=True)), ('a', HardcodedForeignKey(on_delete=models.CASCADE)), ('b', models.ForeignKey('testapp.Author', models.CASCADE))])]
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])

def test_generate_renamed_models_with_dependency_from_hardcoded_fk(self):
    """
    When detecting a renamed model containing a FK whose deconstruct omits
    'to', dependency resolution should still run and produce a RenameModel.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'otherapp.Book'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('testapp', 'OldA', [('id', models.AutoField(primary_key=True)), ('bk', HardcodedForeignKey(on_delete=models.CASCADE))])]
    after = [ModelState('testapp', 'NewA', [('id', models.AutoField(primary_key=True)), ('bk', HardcodedForeignKey(on_delete=models.CASCADE))])]
    after.append(ModelState('otherapp', 'Book', [('id', models.AutoField(primary_key=True))]))
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])

def test_rename_model_with_hardcoded_fk_and_through_field(self):
    """
    A rename involving a model that has both a hardcoded FK (deconstruct
    omitting 'to') and a ManyToMany through= specification shouldn't raise.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('testapp', 'OldWithThrough', [('id', models.AutoField(primary_key=True)), ('author', HardcodedForeignKey(on_delete=models.CASCADE)), ('publishers', models.ManyToManyField('testapp.Publisher', through='testapp.Contract'))]), ModelState('testapp', 'Publisher', [('id', models.AutoField(primary_key=True))]), ModelState('testapp', 'Contract', [('id', models.AutoField(primary_key=True)), ('author', HardcodedForeignKey(on_delete=models.CASCADE)), ('publisher', models.ForeignKey('testapp.Publisher', models.CASCADE))])]
    after = [ModelState('testapp', 'NewWithThrough', [('id', models.AutoField(primary_key=True)), ('author', HardcodedForeignKey(on_delete=models.CASCADE)), ('publishers', models.ManyToManyField('testapp.Publisher', through='testapp.Contract'))]), ModelState('testapp', 'Publisher', [('id', models.AutoField(primary_key=True))]), ModelState('testapp', 'Contract', [('id', models.AutoField(primary_key=True)), ('author', HardcodedForeignKey(on_delete=models.CASCADE)), ('publisher', models.ForeignKey('testapp.Publisher', models.CASCADE))])]
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])

def test_only_relation_agnostic_fields_regression_1(self):
    """Single custom ForeignKey.deconstruct() that removes 'to' should not error."""

    class HardcodedFK(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    field = HardcodedFK(on_delete=models.CASCADE)
    decons = autodetector.only_relation_agnostic_fields({'f': field})
    self.assertEqual(len(decons), 1)
    path, args, kwargs = decons[0]
    self.assertIsInstance(path, str)
    self.assertNotIn('to', kwargs)

def test_only_relation_agnostic_fields_regression_2(self):
    """Multiple fields whose deconstruct remove 'to' should not error."""

    class HardcodedFK(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    a = HardcodedFK(on_delete=models.CASCADE)
    b = HardcodedFK(on_delete=models.CASCADE)
    decons = autodetector.only_relation_agnostic_fields({'a': a, 'b': b})
    self.assertEqual(len(decons), 2)
    for path, args, kwargs in decons:
        self.assertNotIn('to', kwargs)

def test_only_relation_agnostic_fields_regression_3_mixed_with_normal_fk(self):
    """Mix of custom deconstruct removing 'to' and normal FK (with 'to') should not error."""

    class HardcodedFK(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    custom = HardcodedFK(on_delete=models.CASCADE)
    normal = models.ForeignKey('testapp.Author', models.CASCADE)
    decons = autodetector.only_relation_agnostic_fields({'z_field': custom, 'a_field': normal})
    self.assertEqual(len(decons), 2)
    for path, args, kwargs in decons:
        self.assertNotIn('to', kwargs)

def test_only_relation_agnostic_fields_regression_4_many_to_many_like(self):
    """A ManyToManyField subclass that removes 'to' in deconstruct shouldn't error."""

    class HardcodedM2M(models.ManyToManyField):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Publisher'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    m2m = HardcodedM2M()
    decons = autodetector.only_relation_agnostic_fields({'m2m': m2m})
    self.assertEqual(len(decons), 1)
    self.assertNotIn('to', decons[0][2])

def test_only_relation_agnostic_fields_regression_5_foreignobject(self):
    """A ForeignObject subclass that removes 'to' in deconstruct shouldn't error."""

    class HardcodedForeignObject(models.ForeignObject):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'app.Foo'
            super().__init__('app.Foo', models.CASCADE, from_fields=('a',), to_fields=('b',))

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fo = HardcodedForeignObject()
    decons = autodetector.only_relation_agnostic_fields({'fo': fo})
    self.assertEqual(len(decons), 1)
    self.assertNotIn('to', decons[0][2])

def test_only_relation_agnostic_fields_regression_6_preserve_other_kwargs(self):
    """Ensure other kwargs survive and only 'to' is dropped (if present)."""

    class HardcodedFK(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    f = HardcodedFK(on_delete=models.CASCADE, db_column='col_x')
    decons = autodetector.only_relation_agnostic_fields({'f': f})
    self.assertEqual(len(decons), 1)
    path, args, kwargs = decons[0]
    self.assertNotIn('to', kwargs)
    self.assertIn('db_column', kwargs)
    self.assertEqual(kwargs['db_column'], 'col_x')

def test_only_relation_agnostic_fields_regression_7_sorting_behavior(self):
    """Fields are iterated in sorted order of their names; ensure stable output ordering."""

    class HardcodedFK(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'z': HardcodedFK(on_delete=models.CASCADE), 'a': HardcodedFK(on_delete=models.CASCADE)}
    decons = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(decons), 2)

def test_only_relation_agnostic_fields_regression_8_existing_to_key_removed(self):
    """When 'to' exists in the deconstruction it should be removed (pop path)."""
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fk = models.ForeignKey('testapp.Author', models.CASCADE)
    decons = autodetector.only_relation_agnostic_fields({'f': fk})
    self.assertEqual(len(decons), 1)
    self.assertNotIn('to', decons[0][2])

def test_only_relation_agnostic_fields_regression_9_mixed_present_missing(self):
    """Mixed case: one field has 'to' in deconstruct, other doesn't. Both should be fine."""

    class HardcodedFK(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    normal = models.ForeignKey('testapp.Author', models.CASCADE)
    custom = HardcodedFK(on_delete=models.CASCADE)
    decons = autodetector.only_relation_agnostic_fields({'one': normal, 'two': custom})
    self.assertEqual(len(decons), 2)
    for path, args, kwargs in decons:
        self.assertNotIn('to', kwargs)

def test_only_relation_agnostic_fields_regression_10_integration_detect_changes(self):
    """Integration: running _detect_changes with a model that has a field whose deconstruct omits 'to' should not raise."""

    class HardcodedFK(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = self.make_project_state([self.author_empty])
    book = ModelState('testapp', 'Book', [('id', models.AutoField(primary_key=True)), ('author', HardcodedFK(on_delete=models.CASCADE))])
    after = self.make_project_state([self.author_empty, book])
    autodetector = MigrationAutodetector(before, after)
    changes = autodetector._detect_changes()
    self.assertIn('testapp', changes)
    self.assertTrue(any((isinstance(op, operations.CreateModel) for m in changes['testapp'] for op in m.operations)))

from types import SimpleNamespace
from types import SimpleNamespace
from unittest import mock
from django.test import SimpleTestCase
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.state import ProjectState

class OnlyRelationAgnosticFieldsTests(SimpleTestCase):

    def setUp(self):
        self.autodetector = MigrationAutodetector(ProjectState(), ProjectState())

from django.test import SimpleTestCase
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.state import ProjectState
from django.db import migrations

class OnlyRelationAgnosticFieldsTests(SimpleTestCase):

    def make_autodetector(self):
        return MigrationAutodetector(ProjectState(), ProjectState())

from django.test import SimpleTestCase
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.state import ProjectState
import re

def test_only_relation_agnostic_fields_handles_custom_fk_deconstruct_missing_to(self):
    """
    A ForeignKey subclass that removes 'to' from its deconstruct() result
    should be handled without raising KeyError.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    field = HardcodedForeignKey(on_delete=models.CASCADE)
    autodetector = MigrationAutodetector(ProjectState(), ProjectState())
    fields_def = autodetector.only_relation_agnostic_fields({'author': field})
    self.assertEqual(len(fields_def), 1)
    self.assertNotIn('to', fields_def[0][2])

def test_only_relation_agnostic_fields_handles_multiple_fields_with_and_without_to(self):
    """
    Mixed dict of a normal ForeignKey and a custom ForeignKey that omits 'to'
    should be processed without error and both deconstructions should not
    include 'to' afterwards.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    normal_fk = models.ForeignKey('testapp.Author', models.CASCADE)
    custom_fk = HardcodedForeignKey(on_delete=models.CASCADE)
    autodetector = MigrationAutodetector(ProjectState(), ProjectState())
    fields = {'a': normal_fk, 'b': custom_fk}
    fields_def = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(fields_def), 2)
    for decon in fields_def:
        self.assertNotIn('to', decon[2])

def test_only_relation_agnostic_fields_handles_custom_foreignobject_missing_to(self):
    """
    A ForeignObject-like subclass that removes 'to' from deconstruct()
    should not cause a KeyError when processed.
    """

    class CustomForeignObject(models.ForeignObject):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, from_fields=('id',), to_fields=('id',), **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    field = CustomForeignObject(on_delete=models.CASCADE)
    autodetector = MigrationAutodetector(ProjectState(), ProjectState())
    fields_def = autodetector.only_relation_agnostic_fields({'author': field})
    self.assertEqual(len(fields_def), 1)
    self.assertNotIn('to', fields_def[0][2])

def test_only_relation_agnostic_fields_integration_create_model_with_custom_fk(self):
    """
    Integration: creating a model that uses a ForeignKey subclass whose
    deconstruct omits 'to' should produce a CreateModel migration (no crash).
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    book_state = ModelState('testapp', 'Book', [('id', models.AutoField(primary_key=True)), ('author', HardcodedForeignKey(on_delete=models.CASCADE))])
    changes = self.get_changes([], [self.author_empty, book_state])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel'])
    self.assertOperationAttributes(changes, 'testapp', 0, 0, name='Book')

def test_only_relation_agnostic_fields_integration_add_field_custom_fk(self):
    """
    Integration: adding a field that's a custom ForeignKey (deconstruct lacks 'to')
    to an existing app should not raise and should result in an AddField.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [self.author_empty]
    after = [self.author_empty, ModelState('testapp', 'Book', [('id', models.AutoField(primary_key=True)), ('author', HardcodedForeignKey(on_delete=models.CASCADE))])]
    changes = self.get_changes(before, after)
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertIn('CreateModel', [op.__class__.__name__ for op in changes['testapp'][0].operations])

def test_only_relation_agnostic_fields_integration_rename_model_detection_with_custom_fk(self):
    """
    When detecting renamed models, only_relation_agnostic_fields is used to
    compare fields. Ensure a Custom FK that removes 'to' doesn't break
    rename detection.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Publisher'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('testapp', 'OldBook', [('id', models.AutoField(primary_key=True)), ('publisher', HardcodedForeignKey(on_delete=models.CASCADE))])]
    after = [ModelState('testapp', 'NewBook', [('id', models.AutoField(primary_key=True)), ('publisher', HardcodedForeignKey(on_delete=models.CASCADE))])]
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['RenameModel'])

def test_only_relation_agnostic_fields_handles_custom_fk_in_m2m_through(self):
    """
    A through model that contains custom ForeignKeys whose deconstruct omits
    'to' should not cause KeyError when the through mapping is generated.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    contract = ModelState('testapp', 'Contract', [('id', models.AutoField(primary_key=True)), ('author', HardcodedForeignKey(on_delete=models.CASCADE)), ('publisher', HardcodedForeignKey(on_delete=models.CASCADE))])
    author = ModelState('testapp', 'Author', [('id', models.AutoField(primary_key=True))])
    publisher = ModelState('testapp', 'Publisher', [('id', models.AutoField(primary_key=True))])
    changes = self.get_changes([], [author, publisher, contract])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertIn('CreateModel', [op.__class__.__name__ for op in changes['testapp'][0].operations])

def test_only_relation_agnostic_fields_handles_multiple_custom_fks_sorted(self):
    """
    Ensure handling of multiple custom FKs (sorted order of dict keys) does not
    raise; verifies loop/indexing logic is robust to multiple misses of 'to'.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    fields = {'a': HardcodedForeignKey(on_delete=models.CASCADE), 'b': HardcodedForeignKey(on_delete=models.CASCADE), 'c': HardcodedForeignKey(on_delete=models.CASCADE)}
    autodetector = MigrationAutodetector(ProjectState(), ProjectState())
    fields_def = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(fields_def), 3)
    for decon in fields_def:
        self.assertNotIn('to', decon[2])

def test_only_relation_agnostic_fields_custom_fk_hardcoded_to(self):
    """
    A ForeignKey subclass that hardcodes 'to' in __init__ but removes it in
    deconstruct() should not raise and should produce a deconstruction
    without 'to'.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    detector = MigrationAutodetector(ProjectState(), ProjectState())
    fk = HardcodedForeignKey(on_delete=models.CASCADE)
    fields = {'related': fk}
    result = detector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    self.assertNotIn('to', result[0][2])

def test_only_relation_agnostic_fields_mixed_normal_and_custom_fk(self):
    """
    A mix of a normal ForeignKey (which normally deconstructs with 'to')
    and a custom FK that removes 'to' should both be handled without error
    and both should not expose 'to' in the relation-agnostic output.
    """

    class HardcodedForeignKey(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    detector = MigrationAutodetector(ProjectState(), ProjectState())
    normal_fk = models.ForeignKey('testapp.Author', on_delete=models.CASCADE)
    custom_fk = HardcodedForeignKey(on_delete=models.CASCADE)
    fields = {'a_field': normal_fk, 'b_field': custom_fk}
    result = detector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 2)
    for deconstructed in result:
        self.assertNotIn('to', deconstructed[2])

def test_only_relation_agnostic_fields_custom_m2m_field(self):
    """
    A ManyToManyField subclass that strips 'to' in deconstruct should not
    raise and should result in kwargs without 'to'.
    """

    class HardcodedM2M(models.ManyToManyField):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Publisher'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    detector = MigrationAutodetector(ProjectState(), ProjectState())
    m2m = HardcodedM2M()
    fields = {'pubs': m2m}
    result = detector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    self.assertNotIn('to', result[0][2])

def test_only_relation_agnostic_fields_preserves_other_kwargs(self):
    """
    Ensure that when 'to' is removed, other kwargs (e.g., db_column) are
    preserved in the returned deconstruction kwargs.
    """

    class HardcodedFKPreserve(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            kwargs['db_column'] = 'my_col'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    detector = MigrationAutodetector(ProjectState(), ProjectState())
    fk = HardcodedFKPreserve(on_delete=models.CASCADE)
    fields = {'x': fk}
    result = detector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    self.assertNotIn('to', result[0][2])
    self.assertIn('db_column', result[0][2])
    self.assertEqual(result[0][2]['db_column'], 'my_col')

def test_only_relation_agnostic_fields_non_relation_field_unchanged(self):
    """
    Non-relation fields should be deconstructed and returned untouched;
    the absence of 'to' must not cause any exception.
    """
    detector = MigrationAutodetector(ProjectState(), ProjectState())
    int_field = models.IntegerField()
    fields = {'num': int_field}
    result = detector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    self.assertNotIn('to', result[0][2])

def test_only_relation_agnostic_fields_sorted_and_pop_no_exception(self):
    """
    Ensure sorting of fields doesn't influence the safe removal of 'to'
    and that no KeyError is raised across multiple entries.
    """

    class HardcodedFK(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            kwargs['db_column'] = 'col'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    detector = MigrationAutodetector(ProjectState(), ProjectState())
    f1 = HardcodedFK(on_delete=models.CASCADE)
    f2 = models.ForeignKey('testapp.Author', on_delete=models.CASCADE)
    fields = {'alpha': f1, 'beta': f2}
    result = detector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 2)
    for deconstructed in result:
        self.assertNotIn('to', deconstructed[2])

def test_only_relation_agnostic_fields_custom_fk_already_missing_to(self):
    """
    If a custom FK's deconstruct already doesn't include 'to', calling the
    method should still work (no KeyError).
    """

    class CustomNoToFK(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            return (name, path, args, {})
    detector = MigrationAutodetector(ProjectState(), ProjectState())
    fk = CustomNoToFK(on_delete=models.CASCADE)
    fields = {'rel': fk}
    result = detector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    self.assertIsInstance(result[0], tuple)
    self.assertIsInstance(result[0][2], dict)
    self.assertNotIn('to', result[0][2])

def test_only_relation_agnostic_fields_foreignobject_like_custom_deconstruct(self):
    """
    A ForeignObject-like instance that sets remote_field.model but whose
    deconstruct omits 'to' should be handled safely.
    """

    class ForeignObjectLike(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            kwargs['custom'] = 42
            return (name, path, args, kwargs)
    detector = MigrationAutodetector(ProjectState(), ProjectState())
    fo = ForeignObjectLike(on_delete=models.CASCADE)
    fields = {'fobj': fo}
    result = detector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    self.assertNotIn('to', result[0][2])
    self.assertEqual(result[0][2].get('custom'), 42)

def test_only_relation_agnostic_fields_large_mixture_stability(self):
    """
    A larger mixture of normal, custom (missing 'to'), and non-relation
    fields should be processed without error and maintain stable ordering.
    """

    class HardcodedFK(models.ForeignKey):

        def __init__(self, *args, **kwargs):
            kwargs['to'] = 'testapp.Author'
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    detector = MigrationAutodetector(ProjectState(), ProjectState())
    fields = {'a_num': models.IntegerField(), 'b_fk': HardcodedFK(on_delete=models.CASCADE), 'c_char': models.CharField(max_length=10), 'd_fk': models.ForeignKey('testapp.Author', on_delete=models.CASCADE)}
    deconstructed = detector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(deconstructed), 4)
    for item in deconstructed:
        self.assertNotIn('to', item[2])

from types import SimpleNamespace
from types import SimpleNamespace
from django.test import SimpleTestCase
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.state import ProjectState

def test_rename_model_with_custom_fk_deconstruct_missing_to(self):

    class HardFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = ModelState('app', 'OldModel', [('id', models.AutoField(primary_key=True)), ('rel', HardFK('otherapp.Target', models.CASCADE))])
    after = ModelState('app', 'NewModel', [('id', models.AutoField(primary_key=True)), ('rel', HardFK('otherapp.Target', models.CASCADE))])
    changes = self.get_changes([before], [after], MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])

def test_rename_model_with_custom_fk_missing_to_and_to_field(self):

    class HardFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = ModelState('app', 'OldModel2', [('id', models.AutoField(primary_key=True)), ('uniq', models.IntegerField(unique=True)), ('fk', HardFK('app.OldModel2', models.CASCADE, to_field='uniq'))])
    after = ModelState('app', 'NewModel2', [('id', models.AutoField(primary_key=True)), ('uniq', models.IntegerField(unique=True)), ('fk', HardFK('app.NewModel2', models.CASCADE, to_field='uniq'))])
    changes = self.get_changes([before], [after], MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])

def test_rename_model_with_custom_fk_primary_key_and_missing_to(self):

    class HardFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = ModelState('app', 'OldPKModel', [('id', HardFK('app.Base', models.CASCADE, primary_key=True))])
    after = ModelState('app', 'NewPKModel', [('id', HardFK('app.Base', models.CASCADE, primary_key=True))])
    changes = self.get_changes([before], [after], MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])

def test_rename_model_with_custom_many_to_many_deconstruct_missing_to(self):

    class HardM2M(models.ManyToManyField):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = ModelState('app', 'OldM2MModel', [('id', models.AutoField(primary_key=True)), ('tags', HardM2M('otherapp.Tag'))])
    after = ModelState('app', 'NewM2MModel', [('id', models.AutoField(primary_key=True)), ('tags', HardM2M('otherapp.Tag'))])
    changes = self.get_changes([before], [after], MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])

def test_only_relation_agnostic_fields_direct_call_handles_missing_to(self):
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))

    class HardFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    fields = {'id': models.AutoField(primary_key=True), 'fk': HardFK('otherapp.X', models.CASCADE)}
    result = autodetector.only_relation_agnostic_fields(fields)
    self.assertIsInstance(result, list)
    self.assertTrue(all((isinstance(x, tuple) for x in result)))

def test_rename_model_with_multiple_fields_including_custom_fk_missing_to(self):

    class HardFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = ModelState('app', 'OldMany', [('id', models.AutoField(primary_key=True)), ('a', models.CharField(max_length=10)), ('b', models.IntegerField()), ('fk', HardFK('otherapp.Z', models.CASCADE))])
    after = ModelState('app', 'NewMany', [('id', models.AutoField(primary_key=True)), ('a', models.CharField(max_length=10)), ('b', models.IntegerField()), ('fk', HardFK('otherapp.Z', models.CASCADE))])
    changes = self.get_changes([before], [after], MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])

def test_rename_model_field_order_different_with_custom_fk_missing_to(self):

    class HardFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = ModelState('app', 'OldOrder', [('id', models.AutoField(primary_key=True)), ('first', models.CharField(max_length=10)), ('fk', HardFK('otherapp.T', models.CASCADE)), ('second', models.IntegerField())])
    after = ModelState('app', 'NewOrder', [('id', models.AutoField(primary_key=True)), ('fk', HardFK('otherapp.T', models.CASCADE)), ('first', models.CharField(max_length=10)), ('second', models.IntegerField())])
    changes = self.get_changes([before], [after], MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])

def test_rename_proxy_model_with_custom_fk_missing_to(self):

    class HardFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = ModelState('app', 'OldProxy', [], {'proxy': True}, ('app.base',))
    after = ModelState('app', 'NewProxy', [('id', models.AutoField(primary_key=True)), ('fk', HardFK('otherapp.Target', models.CASCADE))])
    changes = self.get_changes([before], [after], MigrationQuestioner({'ask_rename_model': True}))
    self.assertTrue(changes)
    self.assertIn('app', changes)

def test_rename_model_with_custom_foreignobject_missing_to(self):

    class HardForeignObject(models.ForeignObject):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = ModelState('app', 'OldFO', [('id', models.AutoField(primary_key=True)), ('f1', models.IntegerField()), ('fo', HardForeignObject('otherapp.Target', models.CASCADE, from_fields=('f1',), to_fields=('id',)))])
    after = ModelState('app', 'NewFO', [('id', models.AutoField(primary_key=True)), ('f1', models.IntegerField()), ('fo', HardForeignObject('otherapp.Target', models.CASCADE, from_fields=('f1',), to_fields=('id',)))])
    changes = self.get_changes([before], [after], MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])

from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.questioner import MigrationQuestioner
from django.db.migrations.state import ModelState, ProjectState
from django.db import models
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.questioner import MigrationQuestioner
from django.db.migrations.state import ModelState, ProjectState
from django.db.migrations.operations import RenameModel, CreateModel
from django.test import SimpleTestCase

class MissingToRegressionTests(SimpleTestCase):

    def setUp(self):
        self.before = ProjectState()
        self.after = ProjectState()

    def _make_autodetector(self):
        return MigrationAutodetector(self.before, self.after)

def test_only_relation_agnostic_fields_handles_fk_without_to_key(self):

    class FKNoTo(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    field = FKNoTo('otherapp.Target', models.CASCADE)
    autodetector = MigrationAutodetector(ProjectState(), ProjectState())
    result = autodetector.only_relation_agnostic_fields({'fk': field})
    self.assertEqual(len(result), 1)
    path, args, kwargs = result[0]
    self.assertNotIn('to', kwargs)

def test_only_relation_agnostic_fields_handles_manytomany_without_to_key(self):

    class M2MNoTo(models.ManyToManyField):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    field = M2MNoTo('otherapp.Target')
    autodetector = MigrationAutodetector(ProjectState(), ProjectState())
    result = autodetector.only_relation_agnostic_fields({'m2m': field})
    self.assertEqual(len(result), 1)
    path, args, kwargs = result[0]
    self.assertNotIn('to', kwargs)

def test_only_relation_agnostic_fields_handles_onetoone_without_to_key(self):

    class O2ONoTo(models.OneToOneField):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    field = O2ONoTo('otherapp.Target', models.CASCADE)
    autodetector = MigrationAutodetector(ProjectState(), ProjectState())
    result = autodetector.only_relation_agnostic_fields({'o2o': field})
    self.assertEqual(len(result), 1)
    path, args, kwargs = result[0]
    self.assertNotIn('to', kwargs)

def test_only_relation_agnostic_fields_handles_foreignobject_without_to_key(self):

    class ForeignObjectNoTo(models.ForeignObject):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    field = ForeignObjectNoTo('otherapp.Target', models.CASCADE, from_fields=('a',), to_fields=('b',))
    autodetector = MigrationAutodetector(ProjectState(), ProjectState())
    result = autodetector.only_relation_agnostic_fields({'fo': field})
    self.assertEqual(len(result), 1)
    path, args, kwargs = result[0]
    self.assertNotIn('to', kwargs)

def test_generate_renamed_models_with_fk_without_to_key(self):

    class FKNoTo(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    target = ModelState('otherapp', 'Target', [('id', models.AutoField(primary_key=True))])
    before_old = ModelState('app', 'OldModel', [('id', models.AutoField(primary_key=True)), ('ref', FKNoTo('otherapp.Target', models.CASCADE))])
    after_new = ModelState('app', 'NewModel', [('id', models.AutoField(primary_key=True)), ('ref', FKNoTo('otherapp.Target', models.CASCADE))])
    changes = self.get_changes([target, before_old], [target, after_new], MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])

def test_generate_renamed_models_with_multiple_fks_without_to_key(self):

    class FKNoTo(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    t1 = ModelState('otherapp', 'T1', [('id', models.AutoField(primary_key=True))])
    t2 = ModelState('otherapp', 'T2', [('id', models.AutoField(primary_key=True))])
    before_old = ModelState('app', 'OldModel', [('id', models.AutoField(primary_key=True)), ('r1', FKNoTo('otherapp.T1', models.CASCADE)), ('r2', FKNoTo('otherapp.T2', models.CASCADE))])
    after_new = ModelState('app', 'NewModel', [('id', models.AutoField(primary_key=True)), ('r1', FKNoTo('otherapp.T1', models.CASCADE)), ('r2', FKNoTo('otherapp.T2', models.CASCADE))])
    changes = self.get_changes([t1, t2, before_old], [t1, t2, after_new], MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])

def test_create_model_with_fk_without_to_key_does_not_raise(self):

    class FKNoTo(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    target = ModelState('otherapp', 'Target', [('id', models.AutoField(primary_key=True))])
    book = ModelState('app', 'Book', [('id', models.AutoField(primary_key=True)), ('target', FKNoTo('otherapp.Target', models.CASCADE))])
    changes = self.get_changes([target], [target, book])
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['CreateModel'])

def test_added_field_dependency_with_fk_no_to(self):

    class FKNoTo(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    target = ModelState('otherapp', 'Target', [('id', models.AutoField(primary_key=True))])
    before = [target]
    after = [target, ModelState('app', 'Holder', [('id', models.AutoField(primary_key=True))]), ModelState('app', 'Referrer', [('id', models.AutoField(primary_key=True)), ('target', FKNoTo('otherapp.Target', models.CASCADE))])]
    changes = self.get_changes(before, after)
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['CreateModel', 'CreateModel'])

def test_mix_fields_with_and_without_to_key(self):

    class FKNoTo(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    normal_fk = models.ForeignKey('otherapp.Target', models.CASCADE)
    missing_to_fk = FKNoTo('otherapp.Target', models.CASCADE)
    autodetector = MigrationAutodetector(ProjectState(), ProjectState())
    result = autodetector.only_relation_agnostic_fields({'a': normal_fk, 'b': missing_to_fk})
    self.assertEqual(len(result), 2)
    for _, _, kwargs in result:
        self.assertNotIn('to', kwargs)

from django.db import models
from django.db.migrations.questioner import MigrationQuestioner
from django.db.migrations.state import ModelState

def _make_states_for_rename(old_model_name, new_model_name, field):
    """
    Helper to build before/after ProjectState lists for rename tests.
    Includes a 'Target' model so relation resolution succeeds.
    """
    before = [ModelState('testapp', old_model_name, [('id', models.AutoField(primary_key=True)), ('target', field if isinstance(field, models.Field) else field[0])]), ModelState('testapp', 'Target', [('id', models.AutoField(primary_key=True))])]
    after = [ModelState('testapp', new_model_name, [('id', models.AutoField(primary_key=True)), ('target', field if isinstance(field, models.Field) else field[1])]), ModelState('testapp', 'Target', [('id', models.AutoField(primary_key=True))])]
    return (before, after)

def test_rename_model_with_custom_fk_deconstruct_missing_to_new(self):
    before, after = _make_states_for_rename('OldModel', 'NewModel', (models.ForeignKey('testapp.Target', models.CASCADE), HardcodedFK(on_delete=models.CASCADE)))
    changes = AutodetectorTests.get_changes(self=AutodetectorTests(), before_states=before, after_states=after, questioner=MigrationQuestioner({'ask_rename_model': True}))
    assert 'testapp' in changes
    AutodetectorTests.assertNumberMigrations(self=AutodetectorTests(), changes=changes, app_label='testapp', number=1)
    AutodetectorTests.assertOperationTypes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, types=['RenameModel'])
    AutodetectorTests.assertOperationAttributes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, operation_position=0, old_name='OldModel', new_name='NewModel')

def test_rename_model_with_custom_fk_deconstruct_missing_to_old(self):
    before, after = _make_states_for_rename('OldModel', 'NewModel', (HardcodedFK(on_delete=models.CASCADE), models.ForeignKey('testapp.Target', models.CASCADE)))
    changes = AutodetectorTests.get_changes(self=AutodetectorTests(), before_states=before, after_states=after, questioner=MigrationQuestioner({'ask_rename_model': True}))
    assert 'testapp' in changes
    AutodetectorTests.assertNumberMigrations(self=AutodetectorTests(), changes=changes, app_label='testapp', number=1)
    AutodetectorTests.assertOperationTypes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, types=['RenameModel'])
    AutodetectorTests.assertOperationAttributes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, operation_position=0, old_name='OldModel', new_name='NewModel')

def test_rename_model_with_custom_onetoone_deconstruct_missing_to_new(self):
    before, after = _make_states_for_rename('OldOne', 'NewOne', (models.OneToOneField('testapp.Target', models.CASCADE), HardcodedOneToOne(on_delete=models.CASCADE)))
    changes = AutodetectorTests.get_changes(self=AutodetectorTests(), before_states=before, after_states=after, questioner=MigrationQuestioner({'ask_rename_model': True}))
    assert 'testapp' in changes
    AutodetectorTests.assertNumberMigrations(self=AutodetectorTests(), changes=changes, app_label='testapp', number=1)
    AutodetectorTests.assertOperationTypes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, types=['RenameModel'])
    AutodetectorTests.assertOperationAttributes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, operation_position=0, old_name='OldOne', new_name='NewOne')

def test_rename_model_with_custom_onetoone_deconstruct_missing_to_old(self):
    before, after = _make_states_for_rename('OldOne', 'NewOne', (HardcodedOneToOne(on_delete=models.CASCADE), models.OneToOneField('testapp.Target', models.CASCADE)))
    changes = AutodetectorTests.get_changes(self=AutodetectorTests(), before_states=before, after_states=after, questioner=MigrationQuestioner({'ask_rename_model': True}))
    assert 'testapp' in changes
    AutodetectorTests.assertNumberMigrations(self=AutodetectorTests(), changes=changes, app_label='testapp', number=1)
    AutodetectorTests.assertOperationTypes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, types=['RenameModel'])
    AutodetectorTests.assertOperationAttributes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, operation_position=0, old_name='OldOne', new_name='NewOne')

def test_rename_model_with_custom_m2m_deconstruct_missing_to_new(self):
    before, after = _make_states_for_rename('OldM', 'NewM', (models.ManyToManyField('testapp.Target'), HardcodedM2M(through=None)))
    changes = AutodetectorTests.get_changes(self=AutodetectorTests(), before_states=before, after_states=after, questioner=MigrationQuestioner({'ask_rename_model': True}))
    assert 'testapp' in changes
    AutodetectorTests.assertNumberMigrations(self=AutodetectorTests(), changes=changes, app_label='testapp', number=1)
    AutodetectorTests.assertOperationTypes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, types=['RenameModel'])
    AutodetectorTests.assertOperationAttributes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, operation_position=0, old_name='OldM', new_name='NewM')

def test_rename_model_with_custom_m2m_deconstruct_missing_to_old(self):
    before, after = _make_states_for_rename('OldM', 'NewM', (HardcodedM2M(through=None), models.ManyToManyField('testapp.Target')))
    changes = AutodetectorTests.get_changes(self=AutodetectorTests(), before_states=before, after_states=after, questioner=MigrationQuestioner({'ask_rename_model': True}))
    assert 'testapp' in changes
    AutodetectorTests.assertNumberMigrations(self=AutodetectorTests(), changes=changes, app_label='testapp', number=1)
    AutodetectorTests.assertOperationTypes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, types=['RenameModel'])
    AutodetectorTests.assertOperationAttributes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, operation_position=0, old_name='OldM', new_name='NewM')

def test_rename_model_with_both_sides_custom_fk_missing_to(self):
    before, after = _make_states_for_rename('OldBoth', 'NewBoth', (HardcodedFK(on_delete=models.CASCADE), HardcodedFK(on_delete=models.CASCADE)))
    changes = AutodetectorTests.get_changes(self=AutodetectorTests(), before_states=before, after_states=after, questioner=MigrationQuestioner({'ask_rename_model': True}))
    assert 'testapp' in changes
    AutodetectorTests.assertNumberMigrations(self=AutodetectorTests(), changes=changes, app_label='testapp', number=1)
    AutodetectorTests.assertOperationTypes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, types=['RenameModel'])
    AutodetectorTests.assertOperationAttributes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, operation_position=0, old_name='OldBoth', new_name='NewBoth')

def test_rename_model_with_custom_fk_and_mixed_field_types(self):
    before = [ModelState('testapp', 'ComplexOld', [('id', models.AutoField(primary_key=True)), ('target', models.ForeignKey('testapp.Target', models.CASCADE)), ('other', models.OneToOneField('testapp.Target', models.CASCADE))]), ModelState('testapp', 'Target', [('id', models.AutoField(primary_key=True))])]
    after = [ModelState('testapp', 'ComplexNew', [('id', models.AutoField(primary_key=True)), ('target', HardcodedFK(on_delete=models.CASCADE)), ('other', HardcodedOneToOne(on_delete=models.CASCADE))]), ModelState('testapp', 'Target', [('id', models.AutoField(primary_key=True))])]
    changes = AutodetectorTests.get_changes(self=AutodetectorTests(), before_states=before, after_states=after, questioner=MigrationQuestioner({'ask_rename_model': True}))
    assert 'testapp' in changes
    AutodetectorTests.assertNumberMigrations(self=AutodetectorTests(), changes=changes, app_label='testapp', number=1)
    AutodetectorTests.assertOperationTypes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, types=['RenameModel'])
    AutodetectorTests.assertOperationAttributes(self=AutodetectorTests(), changes=changes, app_label='testapp', position=0, operation_position=0, old_name='ComplexOld', new_name='ComplexNew')

from types import SimpleNamespace
from types import SimpleNamespace

def test_only_relation_agnostic_fields_custom_fk_without_to(self):

    class NoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    field = NoToFK('testapp.Author', models.CASCADE, db_column='col_x')
    fields = {'ref': field}
    result = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    path, args, kwargs = result[0]
    self.assertNotIn('to', kwargs)
    self.assertIn('db_column', kwargs)
    self.assertEqual(kwargs['db_column'], 'col_x')

def test_only_relation_agnostic_fields_builtin_fk_to_removed(self):
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    field = models.ForeignKey('testapp.Author', models.CASCADE, db_column='col_y')
    fields = {'ref': field}
    result = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    path, args, kwargs = result[0]
    self.assertNotIn('to', kwargs)
    self.assertIn('db_column', kwargs)
    self.assertEqual(kwargs['db_column'], 'col_y')

def test_only_relation_agnostic_fields_custom_m2m_without_to(self):

    class NoToM2M(models.ManyToManyField):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    field = NoToM2M('testapp.Publisher', blank=True)
    fields = {'m2m': field}
    result = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    _, _, kwargs = result[0]
    self.assertNotIn('to', kwargs)

def test_only_relation_agnostic_fields_m2m_with_through_and_missing_to(self):

    class NoToM2MThrough(models.ManyToManyField):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    field = NoToM2MThrough('testapp.Publisher', through='testapp.Contract')
    fields = {'m2m': field}
    result = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    _, _, kwargs = result[0]
    self.assertNotIn('to', kwargs)

def test_only_relation_agnostic_fields_preserves_to_when_remote_model_none(self):

    class CustomField(models.IntegerField):

        def deconstruct(self):
            return ('name', 'path.to.CustomField', (), {'to': 'some.app.Model', 'custom': True})
    field = CustomField()
    field.remote_field = SimpleNamespace(model=None)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    result = autodetector.only_relation_agnostic_fields({'f': field})
    self.assertEqual(len(result), 1)
    _, _, kwargs = result[0]
    self.assertIn('to', kwargs)
    self.assertTrue(kwargs['custom'])

def test_get_changes_create_model_with_custom_fk_without_to(self):

    class NoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    book = ModelState('testapp', 'Book', [('id', models.AutoField(primary_key=True)), ('author', NoToFK('testapp.Author', models.CASCADE))])
    changes = self.get_changes([], [self.author_empty, book])
    self.assertNumberMigrations(changes, 'testapp', 1)
    self.assertOperationTypes(changes, 'testapp', 0, ['CreateModel'])

def test_get_changes_alter_field_to_custom_fk_without_to(self):

    class NoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('app', 'A', [('id', models.AutoField(primary_key=True)), ('ref', models.ForeignKey('app.A', models.CASCADE))])]
    after = [ModelState('app', 'A', [('id', models.AutoField(primary_key=True)), ('ref', NoToFK('app.A', models.CASCADE))])]
    changes = self.get_changes(before, after)
    self.assertTrue('app' in changes)
    self.assertGreaterEqual(len(changes.get('app', [])), 1)

def test_only_relation_agnostic_fields_multiple_mixed_fields(self):

    class NoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'char': models.CharField(max_length=10), 'fk': NoToFK('testapp.Author', models.CASCADE, db_column='x')}
    result = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 2)
    fk_dec = [d for d in result if d[0].endswith('ForeignKey') or 'ForeignKey' in d[0]][0]
    _, _, fk_kwargs = fk_dec
    self.assertNotIn('to', fk_kwargs)
    self.assertEqual(fk_kwargs.get('db_column'), 'x')

def test_deep_deconstruct_handles_nested_kwargs_without_to(self):

    class NoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            kwargs['meta'] = {'inner': models.IntegerField(default=1).deconstruct()[1:][2] if hasattr(models.IntegerField(default=1), 'deconstruct') else {}}
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    field = NoToFK('testapp.Author', models.CASCADE)
    result = autodetector.only_relation_agnostic_fields({'fk': field})
    self.assertEqual(len(result), 1)
    _, _, kwargs = result[0]
    self.assertNotIn('to', kwargs)
    self.assertIsInstance(kwargs.get('meta'), dict)

def test_only_relation_agnostic_fields_handles_foreignkey_without_to(self):

    class NoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    fk = NoToFK('testapp.Foo', on_delete=models.CASCADE)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'fk': fk}
    fields_def = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(fields_def), 1)
    self.assertNotIn('to', fields_def[0][2])

def test_only_relation_agnostic_fields_handles_two_foreignkeys_without_to(self):

    class NoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    fk1 = NoToFK('testapp.Foo', on_delete=models.CASCADE)
    fk2 = NoToFK('testapp.Bar', on_delete=models.CASCADE)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'a': fk1, 'b': fk2}
    fields_def = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(fields_def), 2)
    for defn in fields_def:
        self.assertNotIn('to', defn[2])

def test_only_relation_agnostic_fields_removes_to_when_present(self):
    fk = models.ForeignKey('testapp.Foo', on_delete=models.CASCADE)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'fk': fk}
    fields_def = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(fields_def), 1)
    self.assertNotIn('to', fields_def[0][2])

def test_only_relation_agnostic_fields_handles_many_to_many_without_to(self):

    class NoToM2M(models.ManyToManyField):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    m2m = NoToM2M('testapp.Publisher')
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'publishers': m2m}
    fields_def = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(fields_def), 1)
    self.assertNotIn('to', fields_def[0][2])

def test_only_relation_agnostic_fields_preserves_to_when_remote_field_model_false(self):
    fk = models.ForeignKey('testapp.Foo', on_delete=models.CASCADE)
    fk.remote_field.model = None
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'fk': fk}
    fields_def = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(fields_def), 1)
    self.assertIn('to', fields_def[0][2])

def test_only_relation_agnostic_fields_mixed_field_types(self):

    class NoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    fk = NoToFK('testapp.Foo', on_delete=models.CASCADE)
    char = models.CharField(max_length=10)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'b': char, 'a': fk}
    fields_def = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(fields_def), 2)
    fk_def, char_def = fields_def
    self.assertNotIn('to', fk_def[2])
    self.assertIsInstance(char_def[2], dict)

def test_generate_renamed_models_handles_fk_deconstruct_without_to(self):

    class NoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('app', 'Old', [('id', models.AutoField(primary_key=True)), ('ref', NoToFK('app.Target', on_delete=models.CASCADE))])]
    after = [ModelState('app', 'New', [('id', models.AutoField(primary_key=True)), ('ref', NoToFK('app.Target', on_delete=models.CASCADE))])]
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])
    self.assertOperationAttributes(changes, 'app', 0, 0, old_name='Old', new_name='New')

def test_generate_renamed_fields_handles_fk_deconstruct_without_to(self):

    class NoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('app', 'M', [('id', models.AutoField(primary_key=True)), ('old_name', NoToFK('app.Target', on_delete=models.CASCADE))])]
    after = [ModelState('app', 'M', [('id', models.AutoField(primary_key=True)), ('new_name', NoToFK('app.Target', on_delete=models.CASCADE))])]
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameField'])
    self.assertOperationAttributes(changes, 'app', 0, 0, old_name='old_name', new_name='new_name')

def test_only_relation_agnostic_fields_many_varied_cases(self):

    class NoToFK(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    fk_with_to = models.ForeignKey('app.X', on_delete=models.CASCADE)
    fk_without_to = NoToFK('app.Y', on_delete=models.CASCADE)
    m2m_without_to = models.ManyToManyField('app.Z')
    orig_m2m_deconstruct = m2m_without_to.deconstruct

    def custom_m2m_deconstruct():
        name, path, args, kwargs = orig_m2m_deconstruct()
        kwargs.pop('to', None)
        return (name, path, args, kwargs)
    m2m_without_to.deconstruct = custom_m2m_deconstruct
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'f_with_to': fk_with_to, 'f_without_to': fk_without_to, 'rel': m2m_without_to}
    fields_def = autodetector.only_relation_agnostic_fields(fields)
    for defn in fields_def:
        self.assertNotIn('to', defn[2])

def test_only_relation_agnostic_fields_handles_fk_without_to(self):

    class HardcodedForeignKey(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'ref': HardcodedForeignKey('testapp.Author', models.CASCADE)}
    result = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    self.assertNotIn('to', result[0][2])

def test_only_relation_agnostic_fields_handles_one_to_one_without_to(self):

    class HardcodedOneToOne(models.OneToOneField):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'one': HardcodedOneToOne('testapp.Author', models.CASCADE)}
    result = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    self.assertNotIn('to', result[0][2])

def test_only_relation_agnostic_fields_handles_foreignobject_without_to(self):

    class HardcodedForeignObject(models.ForeignObject):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'fo': HardcodedForeignObject('testapp.Author', models.CASCADE, from_fields=('id',), to_fields=('id',))}
    result = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    self.assertNotIn('to', result[0][2])

def test_only_relation_agnostic_fields_handles_m2m_without_to(self):

    class HardcodedManyToMany(models.ManyToManyField):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'m2m': HardcodedManyToMany('testapp.Publisher')}
    result = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 1)
    self.assertNotIn('to', result[0][2])

def test_generate_renamed_models_with_fk_deconstruct_missing_to(self):

    class HardcodedForeignKey(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('app', 'OldModel', [('id', models.AutoField(primary_key=True)), ('ref', models.ForeignKey('otherapp.Target', models.CASCADE))])]
    after = [ModelState('app', 'NewModel', [('id', models.AutoField(primary_key=True)), ('ref', HardcodedForeignKey('otherapp.Target', models.CASCADE))])]
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])

def test_generate_renamed_models_with_one_to_one_deconstruct_missing_to(self):

    class HardcodedOneToOne(models.OneToOneField):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('app', 'A', [('id', models.AutoField(primary_key=True)), ('link', models.OneToOneField('otherapp.Target', models.CASCADE))])]
    after = [ModelState('app', 'B', [('id', models.AutoField(primary_key=True)), ('link', HardcodedOneToOne('otherapp.Target', models.CASCADE))])]
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])

def test_generate_renamed_models_with_foreignobject_deconstruct_missing_to(self):

    class HardcodedForeignObject(models.ForeignObject):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    before = [ModelState('app', 'X', [('id', models.AutoField(primary_key=True)), ('a', models.IntegerField()), ('b', models.IntegerField()), ('fo', models.ForeignObject('otherapp.Target', models.CASCADE, from_fields=('a',), to_fields=('a',)))])]
    after = [ModelState('app', 'Y', [('id', models.AutoField(primary_key=True)), ('a', models.IntegerField()), ('b', models.IntegerField()), ('fo', HardcodedForeignObject('otherapp.Target', models.CASCADE, from_fields=('a',), to_fields=('a',)))])]
    changes = self.get_changes(before, after, MigrationQuestioner({'ask_rename_model': True}))
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['RenameModel'])

def test_create_model_with_fk_deconstruct_missing_to(self):

    class HardcodedForeignKey(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)
    new_model = ModelState('app', 'Created', [('id', models.AutoField(primary_key=True)), ('ref', HardcodedForeignKey('otherapp.Target', models.CASCADE))])
    changes = self.get_changes([], [new_model])
    self.assertNumberMigrations(changes, 'app', 1)
    self.assertOperationTypes(changes, 'app', 0, ['CreateModel'])

def test_mixed_fields_only_relation_agnostic_fields_no_exception(self):

    class HardcodedForeignKey(models.ForeignKey):

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            kwargs.pop('to', None)
            return (name, path, args, kwargs)

    class NormalForeignKey(models.ForeignKey):
        pass
    autodetector = MigrationAutodetector(self.make_project_state([]), self.make_project_state([]))
    fields = {'a': HardcodedForeignKey('otherapp.Target', models.CASCADE), 'b': NormalForeignKey('otherapp.Target', models.CASCADE), 'c': models.IntegerField()}
    result = autodetector.only_relation_agnostic_fields(fields)
    self.assertEqual(len(result), 3)
    for entry in result:
        self.assertIsInstance(entry, tuple)