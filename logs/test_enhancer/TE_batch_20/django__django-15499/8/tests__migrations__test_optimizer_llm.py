from django.test import SimpleTestCase
from django.db import migrations, models
from django.db.migrations import operations
from django.db.migrations.optimizer import MigrationOptimizer
from django.db.migrations.serializer import serializer_factory

def _serialize(op):
    return serializer_factory(op).serialize()[0]

def test_create_alter_model_managers_case_insensitive(self):
    """
    CreateModel + AlterModelManagers should optimize even if the case differs.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=255))]), migrations.AlterModelManagers(name='foo', managers=[('objects', models.Manager()), ('things', models.Manager())])], [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=255))], managers=[('objects', models.Manager()), ('things', models.Manager())])])

def test_create_alter_model_managers_default_to_custom(self):
    """
    CreateModel that omits managers (uses default) should absorb AlterModelManagers.
    """
    self.assertOptimizesTo([migrations.CreateModel('MyModel', fields=[]), migrations.AlterModelManagers(name='MyModel', managers=[('objects', models.Manager()), ('custom', EmptyManager())])], [migrations.CreateModel('MyModel', fields=[], managers=[('objects', models.Manager()), ('custom', EmptyManager())])])

def test_create_alter_model_managers_duplicate_names_raises(self):
    """
    If AlterModelManagers introduces duplicate manager names, CreateModel
    construction during optimization should raise a ValueError.
    """
    with self.assertRaises(ValueError):
        self.optimize([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('objects', models.Manager()), ('objects', models.Manager())])], 'migrations')

def test_multiple_alter_model_managers_collapses_to_last(self):
    """
    Multiple AlterModelManagers after a CreateModel should result in a single
    CreateModel with the last managers list.
    """
    managers_first = [('objects', models.Manager()), ('a', EmptyManager())]
    managers_second = [('objects', models.Manager()), ('b', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=managers_first), migrations.AlterModelManagers(name='Foo', managers=managers_second)], [migrations.CreateModel('Foo', fields=[], managers=managers_second)])

def test_create_alter_model_managers_then_rename_absorbed(self):
    """
    CreateModel + AlterModelManagers + RenameModel should produce a CreateModel
    for the new name with the managers applied.
    """
    managers = [('objects', EmptyManager()), ('custom', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel(name='Foo', fields=[('name', models.CharField(max_length=255))]), migrations.AlterModelManagers(name='Foo', managers=managers), migrations.RenameModel('Foo', 'Bar')], [migrations.CreateModel('Bar', fields=[('name', models.CharField(max_length=255))], managers=managers)])

def test_create_alter_model_managers_and_delete_disappears(self):
    """
    CreateModel followed by AlterModelManagers and then DeleteModel should
    collapse into nothing.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=255))]), migrations.AlterModelManagers(name='Foo', managers=[('objects', models.Manager()), ('x', EmptyManager())]), migrations.DeleteModel('Foo')], [])

def test_create_alter_model_managers_preserves_options_and_bases(self):
    """
    CreateModel should preserve options and bases while adopting managers from AlterModelManagers.
    """
    managers = [('objects', EmptyManager()), ('mng', EmptyManager())]
    managers_op = [('objects', models.Manager()), ('mng', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel(name='Foo', fields=[('a', models.IntegerField())], options={'verbose_name': 'PrettyFoo'}, bases=(UnicodeModel,), managers=managers), migrations.AlterModelManagers(name='Foo', managers=managers_op)], [migrations.CreateModel(name='Foo', fields=[('a', models.IntegerField())], options={'verbose_name': 'PrettyFoo'}, bases=(UnicodeModel,), managers=managers_op)])

def test_create_alter_model_managers_with_rename_chain(self):
    """
    CreateModel + AlterModelManagers + multiple RenameModel ops should result in a single
    CreateModel with the final name and managers from the AlterModelManagers.
    """
    managers = [('objects', EmptyManager()), ('m', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Alpha', fields=[]), migrations.AlterModelManagers(name='Alpha', managers=managers), migrations.RenameModel('Alpha', 'Beta'), migrations.RenameModel('Beta', 'Gamma')], [migrations.CreateModel('Gamma', fields=[], managers=managers)])

def test_create_alter_model_managers_case_and_serialization(self):
    """
    Ensure manager replacement is considered in serialization comparison,
    and that case-insensitive model naming still results in manager update.
    """
    managers_op = [('objects', models.Manager()), ('extra', EmptyManager())]
    result, _ = self.optimize([migrations.CreateModel('CaseTest', fields=[]), migrations.AlterModelManagers(name='casetest', managers=managers_op)], 'migrations')
    self.assertEqual(len(result), 1)
    serialized = [self.serialize(op) for op in result][0]
    self.assertIn('extra', str(serialized))

from django.db.migrations import operations as migrations_ops
from django.test import SimpleTestCase
from django.db import models, migrations
from django.db.migrations.optimizer import MigrationOptimizer
from django.db.migrations.serializer import serializer_factory
from .models import EmptyManager, UnicodeModel

def serialize(op):
    return serializer_factory(op).serialize()[0]

def test_create_alter_model_managers_merge_custom(self):
    """
    CreateModel followed by AlterModelManagers should collapse into a single
    CreateModel with the new managers (including custom/EmptyManager).
    """
    managers_initial = [('objects', models.Manager())]
    managers_updated = [('objects', models.Manager()), ('things', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[], managers=managers_initial), migrations.AlterModelManagers(name='Foo', managers=managers_updated)], [migrations.CreateModel('Foo', fields=[], managers=managers_updated)])

def test_create_multiple_alter_model_managers_last_wins(self):
    """
    Multiple successive AlterModelManagers should result in the last one
    being applied when combined with CreateModel.
    """
    managers_v1 = [('objects', models.Manager())]
    managers_v2 = [('objects', EmptyManager())]
    managers_v3 = [('objects', models.Manager()), ('alt', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[], managers=managers_v1), migrations.AlterModelManagers(name='Foo', managers=managers_v2), migrations.AlterModelManagers(name='Foo', managers=managers_v3)], [migrations.CreateModel('Foo', fields=[], managers=managers_v3)])

def test_create_addfield_then_alter_managers(self):
    """
    AddField followed by AlterModelManagers should both be merged into the
    CreateModel (field added and managers updated).
    """
    managers_after = [('objects', models.Manager()), ('m', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('a', models.IntegerField())]), migrations.AddField('Foo', 'b', models.CharField(max_length=10)), migrations.AlterModelManagers(name='Foo', managers=managers_after)], [migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.CharField(max_length=10))], managers=managers_after)])

def test_create_alter_managers_then_addfield(self):
    """
    AlterModelManagers before AddField should still result in a single
    CreateModel with both managers and the added field.
    """
    managers_after = [('objects', EmptyManager()), ('extra', models.Manager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('a', models.IntegerField())]), migrations.AlterModelManagers(name='Foo', managers=managers_after), migrations.AddField('Foo', 'b', models.IntegerField())], [migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())], managers=managers_after)])

def test_create_rename_field_and_alter_managers(self):
    """
    RenameField combined with AlterModelManagers should be reflected in the
    single CreateModel (field renamed, managers updated).
    """
    managers_after = [('objects', models.Manager()), ('x', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('old', models.CharField(max_length=20))]), migrations.RenameField('Foo', 'old', 'new'), migrations.AlterModelManagers(name='Foo', managers=managers_after)], [migrations.CreateModel('Foo', fields=[('new', models.CharField(max_length=20))], managers=managers_after)])

def test_create_remove_field_and_alter_managers(self):
    """
    RemoveField combined with AlterModelManagers should result in CreateModel
    without the removed field and with managers updated.
    """
    managers_after = [('objects', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('keep', models.IntegerField()), ('drop', models.IntegerField())]), migrations.RemoveField('Foo', 'drop'), migrations.AlterModelManagers(name='Foo', managers=managers_after)], [migrations.CreateModel('Foo', fields=[('keep', models.IntegerField())], managers=managers_after)])

def test_create_alter_options_and_alter_managers(self):
    """
    AlterModelOptions and AlterModelManagers combined with CreateModel should
    produce a CreateModel with both the updated options and managers.
    """
    managers_after = [('objects', models.Manager()), ('alt', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelOptions(name='Foo', options={'verbose_name': 'X'}), migrations.AlterModelManagers(name='Foo', managers=managers_after)], [migrations.CreateModel('Foo', fields=[], options={'verbose_name': 'X'}, managers=managers_after)])

def test_create_alter_unique_and_alter_managers(self):
    """
    AlterUniqueTogether and AlterModelManagers should both be merged into the
    initial CreateModel operation.
    """
    managers_after = [('objects', EmptyManager())]
    alter_unique = migrations.AlterUniqueTogether('Foo', [['a', 'b']])
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())]), alter_unique, migrations.AlterModelManagers(name='Foo', managers=managers_after)], [migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())], options={'unique_together': set([('a', 'b')])}, managers=managers_after)])

def test_create_alter_order_with_respect_to_and_alter_managers(self):
    """
    AlterOrderWithRespectTo and AlterModelManagers should both be applied to
    the CreateModel when optimizing.
    """
    managers_after = [('objects', models.Manager()), ('alt', EmptyManager())]
    alter_owrt = migrations.AlterOrderWithRespectTo('Foo', 'a')
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('a', models.IntegerField())]), alter_owrt, migrations.AlterModelManagers(name='Foo', managers=managers_after)], [migrations.CreateModel('Foo', fields=[('a', models.IntegerField())], options={'order_with_respect_to': 'a'}, managers=managers_after)])

def test_alter_managers_for_different_model_does_not_merge(self):
    """
    AlterModelManagers for a different model should not be applied to the
    CreateModel.
    """
    managers_other = [('objects', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Bar', managers=managers_other)], [migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Bar', managers=managers_other)])

def test_create_model_add_field_then_alter_managers(self):
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AddField('Foo', 'a', models.IntegerField()), migrations.AlterModelManagers(name='Foo', managers=[('objects', EmptyManager()), ('things', EmptyManager())])], [migrations.CreateModel('Foo', fields=[('a', models.IntegerField())], managers=[('objects', EmptyManager()), ('things', EmptyManager())])])

def test_create_model_alter_field_then_alter_managers(self):
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('a', models.IntegerField())]), migrations.AlterField('Foo', 'a', models.CharField(max_length=10)), migrations.AlterModelManagers(name='Foo', managers=[('objects', EmptyManager()), ('m', EmptyManager())])], [migrations.CreateModel('Foo', fields=[('a', models.CharField(max_length=10))], managers=[('objects', EmptyManager()), ('m', EmptyManager())])])

def test_create_model_remove_field_then_alter_managers(self):
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())]), migrations.RemoveField('Foo', 'b'), migrations.AlterModelManagers(name='Foo', managers=[('objects', EmptyManager()), ('mgr', EmptyManager())])], [migrations.CreateModel('Foo', fields=[('a', models.IntegerField())], managers=[('objects', EmptyManager()), ('mgr', EmptyManager())])])

def test_create_model_rename_field_then_alter_managers(self):
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())]), migrations.RenameField('Foo', 'b', 'c'), migrations.AlterModelManagers(name='Foo', managers=[('objects', EmptyManager()), ('m2', EmptyManager())])], [migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('c', models.IntegerField())], managers=[('objects', EmptyManager()), ('m2', EmptyManager())])])

def test_create_model_add_field_with_reordering_and_alter_managers(self):
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.CreateModel('Bar', fields=[('size', models.IntegerField())]), migrations.AddField('Foo', 'link', models.ForeignKey('migrations.Bar', models.CASCADE)), migrations.AlterModelManagers(name='Foo', managers=[('objects', EmptyManager()), ('custom', EmptyManager())])], [migrations.CreateModel('Bar', fields=[('size', models.IntegerField())]), migrations.CreateModel('Foo', fields=[('link', models.ForeignKey('migrations.Bar', models.CASCADE))], managers=[('objects', EmptyManager()), ('custom', EmptyManager())])])

def test_create_alter_managers_then_delete_collapse(self):
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('objects', EmptyManager())]), migrations.DeleteModel('Foo')], [])

def test_remove_field_updates_unique_together_with_managers(self):
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())], options={'unique_together': {('b', 'a')}}), migrations.RemoveField('Foo', 'b'), migrations.AlterModelManagers(name='Foo', managers=[('objects', EmptyManager()), ('m', EmptyManager())])], [migrations.CreateModel('Foo', fields=[('a', models.IntegerField())], managers=[('objects', EmptyManager()), ('m', EmptyManager())])])

def test_rename_field_updates_unique_together_with_managers(self):
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('old', models.IntegerField()), ('x', models.IntegerField())], options={'unique_together': {('old', 'x')}}), migrations.RenameField('Foo', 'old', 'new'), migrations.AlterModelManagers(name='Foo', managers=[('objects', EmptyManager()), ('mm', EmptyManager())])], [migrations.CreateModel('Foo', fields=[('new', models.IntegerField()), ('x', models.IntegerField())], options={'unique_together': {('new', 'x')}}, managers=[('objects', EmptyManager()), ('mm', EmptyManager())])])

def test_order_with_respect_to_removed_and_managers_applied(self):
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())], options={'order_with_respect_to': 'b'}), migrations.RemoveField('Foo', 'b'), migrations.AlterModelManagers(name='Foo', managers=[('objects', EmptyManager()), ('m', EmptyManager())])], [migrations.CreateModel('Foo', fields=[('a', models.IntegerField())], managers=[('objects', EmptyManager()), ('m', EmptyManager())])])

def test_field_operations_surrounding_alter_managers(self):
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AddField('Foo', 'a', models.IntegerField()), migrations.AlterModelManagers(name='Foo', managers=[('objects', EmptyManager())]), migrations.AlterField('Foo', 'a', models.BigIntegerField())], [migrations.CreateModel('Foo', fields=[('a', models.BigIntegerField())], managers=[('objects', EmptyManager())])])

def test_create_alter_model_managers_simple_merge(self):
    """
    CreateModel followed by AlterModelManagers should merge managers into
    the CreateModel.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('objects', models.Manager()), ('things', models.Manager())])], [migrations.CreateModel('Foo', fields=[], managers=[('objects', models.Manager()), ('things', models.Manager())])])

def test_create_alter_model_managers_no_initial_managers(self):
    """
    CreateModel with no managers (relying on default) followed by
    AlterModelManagers should produce CreateModel with the provided managers.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('objects', models.Manager()), ('custom', EmptyManager())])], [migrations.CreateModel('Foo', fields=[], managers=[('objects', models.Manager()), ('custom', EmptyManager())])])

def test_create_alter_model_managers_case_insensitive_name(self):
    """
    The matching between CreateModel and AlterModelManagers should be
    case-insensitive.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='foo', managers=[('objects', models.Manager()), ('custom', EmptyManager())])], [migrations.CreateModel('Foo', fields=[], managers=[('objects', models.Manager()), ('custom', EmptyManager())])])

def test_create_alter_model_managers_preserve_options_and_bases(self):
    """
    Options and bases on CreateModel should be preserved when absorbing
    AlterModelManagers.
    """
    managers = [('objects', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel(name='Foo', fields=[('name', models.CharField(max_length=50))], options={'verbose_name': 'Foo'}, bases=(UnicodeModel,), managers=managers), migrations.AlterModelManagers(name='Foo', managers=[('objects', EmptyManager()), ('custom', EmptyManager())])], [migrations.CreateModel(name='Foo', fields=[('name', models.CharField(max_length=50))], options={'verbose_name': 'Foo'}, bases=(UnicodeModel,), managers=[('objects', EmptyManager()), ('custom', EmptyManager())])])

def test_multiple_alter_model_managers_chain(self):
    """
    Multiple AlterModelManagers after a CreateModel should result in a single
    CreateModel with the last-provided managers.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('a', EmptyManager())]), migrations.AlterModelManagers(name='Foo', managers=[('b', EmptyManager())])], [migrations.CreateModel('Foo', fields=[], managers=[('b', EmptyManager())])])

def test_create_alter_managers_then_delete_model_collapses(self):
    """
    CreateModel followed by AlterModelManagers and DeleteModel should
    collapse to nothing (Create + Delete).
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('custom', EmptyManager())]), migrations.DeleteModel('Foo')], [])

def test_create_rename_then_alter_model_managers(self):
    """
    A RenameModel followed by AlterModelManagers of the new name should be
    absorbed by the CreateModel renamed accordingly with updated managers.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.RenameModel('Foo', 'Bar'), migrations.AlterModelManagers(name='Bar', managers=[('custom', EmptyManager())])], [migrations.CreateModel('Bar', fields=[], managers=[('custom', EmptyManager())])])

def test_create_alter_model_managers_preserve_fields(self):
    """
    Absorbing AlterModelManagers must not alter the CreateModel fields.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.CharField(max_length=10))]), migrations.AlterModelManagers(name='Foo', managers=[('m', EmptyManager())])], [migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.CharField(max_length=10))], managers=[('m', EmptyManager())])])

def test_create_alter_model_managers_with_existing_managers_replaced(self):
    """
    If CreateModel already has managers, AlterModelManagers should replace
    them entirely in the optimized CreateModel.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[], managers=[('objects', EmptyManager())]), migrations.AlterModelManagers(name='Foo', managers=[('repl', EmptyManager())])], [migrations.CreateModel('Foo', fields=[], managers=[('repl', EmptyManager())])])

def test_create_alter_model_managers_case_insensitive(self):
    """
    AlterModelManagers name matching should be case-insensitive when merged
    into a preceding CreateModel.
    """
    ops = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20))]), migrations.AlterModelManagers('foo', managers=[('objects', models.Manager()), ('things', models.Manager())])]
    expected = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20))], managers=[('objects', models.Manager()), ('things', models.Manager())])]
    self.assertOptimizesTo(ops, expected)

def test_create_addfield_then_alter_managers(self):
    """
    CreateModel + AddField + AlterModelManagers should result in a single
    CreateModel with the added field and the new managers.
    """
    ops = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20))]), migrations.AddField('Foo', 'age', models.IntegerField()), migrations.AlterModelManagers('Foo', managers=[('objects', models.Manager()), ('m2', models.Manager())])]
    expected = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20)), ('age', models.IntegerField())], managers=[('objects', models.Manager()), ('m2', models.Manager())])]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_managers_then_addfield(self):
    """
    CreateModel + AlterModelManagers + AddField should also collapse into a
    single CreateModel with managers and the added field.
    """
    ops = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20))]), migrations.AlterModelManagers('Foo', managers=[('objects', models.Manager()), ('m2', models.Manager())]), migrations.AddField('Foo', 'age', models.IntegerField())]
    expected = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20)), ('age', models.IntegerField())], managers=[('objects', models.Manager()), ('m2', models.Manager())])]
    self.assertOptimizesTo(ops, expected)

def test_create_rename_field_then_alter_managers(self):
    """
    CreateModel + RenameField + AlterModelManagers should produce a single
    CreateModel with the renamed field and updated managers.
    """
    ops = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20))]), migrations.RenameField('Foo', 'name', 'title'), migrations.AlterModelManagers('Foo', managers=[('objects', models.Manager()), ('m3', models.Manager())])]
    expected = [migrations.CreateModel('Foo', fields=[('title', models.CharField(max_length=20))], managers=[('objects', models.Manager()), ('m3', models.Manager())])]
    self.assertOptimizesTo(ops, expected)

def test_create_remove_field_then_alter_managers(self):
    """
    CreateModel + RemoveField + AlterModelManagers should produce a single
    CreateModel with the remaining fields and updated managers.
    """
    ops = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20)), ('age', models.IntegerField())]), migrations.RemoveField('Foo', 'age'), migrations.AlterModelManagers('Foo', managers=[('objects', models.Manager()), ('m4', models.Manager())])]
    expected = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20))], managers=[('objects', models.Manager()), ('m4', models.Manager())])]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_managers_and_delete(self):
    """
    CreateModel followed by AlterModelManagers and then DeleteModel should
    collapse entirely (no leftover AlterModelManagers).
    """
    ops = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20))]), migrations.AlterModelManagers('Foo', managers=[('objects', models.Manager()), ('m5', models.Manager())]), migrations.DeleteModel('Foo')]
    expected = []
    self.assertOptimizesTo(ops, expected)

def test_multiple_alter_model_managers(self):
    """
    Multiple consecutive AlterModelManagers should result in the final one
    being applied to the CreateModel.
    """
    ops = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20))]), migrations.AlterModelManagers('Foo', managers=[('objects', models.Manager()), ('first', models.Manager())]), migrations.AlterModelManagers('Foo', managers=[('objects', models.Manager()), ('second', models.Manager())])]
    expected = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20))], managers=[('objects', models.Manager()), ('second', models.Manager())])]
    self.assertOptimizesTo(ops, expected)

def test_alter_managers_different_model_does_not_merge(self):
    """
    AlterModelManagers for a different model should not be merged into the
    CreateModel.
    """
    ops = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=20))]), migrations.AlterModelManagers('Bar', managers=[('objects', models.Manager()), ('x', models.Manager())])]
    self.assertOptimizesTo(ops, ops)

def test_create_alter_model_options_and_managers(self):
    """
    CreateModel + AlterModelOptions + AlterModelManagers should result in a
    single CreateModel with both options and managers applied.
    """
    ops = [migrations.CreateModel('Foo', fields=[], options={'verbose_name': 'Foo'}), migrations.AlterModelOptions('Foo', options={'verbose_name_plural': 'Foos'}), migrations.AlterModelManagers('Foo', managers=[('objects', models.Manager()), ('m6', models.Manager())])]
    expected = [migrations.CreateModel('Foo', fields=[], options={'verbose_name_plural': 'Foos'}, managers=[('objects', models.Manager()), ('m6', models.Manager())])]
    self.assertOptimizesTo(ops, expected)