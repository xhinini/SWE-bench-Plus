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