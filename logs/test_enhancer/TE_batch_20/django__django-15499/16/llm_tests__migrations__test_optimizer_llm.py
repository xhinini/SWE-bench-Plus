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

def test_merge_alter_managers_case_insensitive(self):
    """
    CreateModel followed by AlterModelManagers with a different-cased model
    name should optimize into a single CreateModel.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='foo', managers=[('m', models.Manager())])], [migrations.CreateModel('Foo', fields=[], managers=[('m', models.Manager())])])

def test_create_alter_model_options_then_managers(self):
    """
    CreateModel followed by AlterModelOptions and AlterModelManagers should
    result in a single CreateModel with both options and managers applied.
    """
    managers = [('objects', models.Manager()), ('extra', models.Manager())]
    self.assertOptimizesTo([migrations.CreateModel(name='Foo', fields=[], options={'verbose_name': 'Orig'}), migrations.AlterModelOptions(name='Foo', options={'verbose_name_plural': 'Foos'}), migrations.AlterModelManagers(name='Foo', managers=managers)], [migrations.CreateModel(name='Foo', fields=[], options={'verbose_name': 'Orig', 'verbose_name_plural': 'Foos'}, managers=managers)])

def test_create_alter_managers_then_delete_model(self):
    """
    CreateModel + AlterModelManagers + DeleteModel should collapse into nothing.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('m', models.Manager())]), migrations.DeleteModel('Foo')], [])

def test_create_rename_then_alter_managers_merges(self):
    """
    CreateModel absorbed into RenameModel and then AlterModelManagers should
    yield a CreateModel with the new name and the managers applied.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.RenameModel('Foo', 'Bar'), migrations.AlterModelManagers(name='Bar', managers=[('m', models.Manager())])], [migrations.CreateModel('Bar', fields=[], managers=[('m', models.Manager())])])

def test_multiple_alter_managers_last_wins(self):
    """
    Multiple AlterModelManagers following a CreateModel should result in a
    CreateModel using the managers from the last AlterModelManagers.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('a', models.Manager())]), migrations.AlterModelManagers(name='Foo', managers=[('b', models.Manager())])], [migrations.CreateModel('Foo', fields=[], managers=[('b', models.Manager())])])

def test_create_with_default_objects_manager_removed_after_merge(self):
    """
    If AlterModelManagers sets managers to the default ('objects', Manager()),
    the resulting CreateModel should omit the managers argument (deconstruction
    behavior), i.e. equivalent to CreateModel(..., managers not provided).
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('objects', models.Manager())])], [migrations.CreateModel('Foo', fields=[])])

def test_create_with_field_ops_and_alter_managers(self):
    """
    Field operations between CreateModel and AlterModelManagers should be
    absorbed too, resulting in a CreateModel with the added/altered fields
    and the new managers.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[('a', models.IntegerField())]), migrations.AddField('Foo', 'b', models.CharField(max_length=10)), migrations.AlterModelManagers(name='Foo', managers=[('m', models.Manager())])], [migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.CharField(max_length=10))], managers=[('m', models.Manager())])])

def test_create_alter_field_and_managers_merge(self):
    """
    AlterField and AlterModelManagers after CreateModel should both be
    absorbed into a single CreateModel summarizing both changes.
    """
    managers = [('objects', models.Manager()), ('mgr', models.Manager())]
    self.assertOptimizesTo([migrations.CreateModel(name='Foo', fields=[('name', models.CharField(max_length=50))]), migrations.AlterField('Foo', 'name', models.TextField()), migrations.AlterModelManagers(name='Foo', managers=managers)], [migrations.CreateModel(name='Foo', fields=[('name', models.TextField())], managers=managers)])

def test_create_alter_managers_with_non_default_app_label(self):
    """
    Ensure the CreateModel+AlterModelManagers merge works regardless of the
    app_label passed to the optimizer.
    """
    ops = [migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('m', models.Manager())])]
    result, _ = self.optimize(ops, app_label='custom_app')
    result = [self.serialize(f) for f in result]
    expected = [self.serialize(migrations.CreateModel('Foo', fields=[], managers=[('m', models.Manager())]))]
    self.assertEqual(expected, result)

def test_create_then_alter_managers_simple_variant_1(self):
    """
    Simple CreateModel followed by AlterModelManagers should merge into a
    single CreateModel with the new managers.
    """
    managers = [('objects', models.Manager()), ('things', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', [('name', models.CharField(max_length=255))]), migrations.AlterModelManagers(name='Foo', managers=managers)], [migrations.CreateModel('Foo', [('name', models.CharField(max_length=255))], managers=managers)])

def test_create_with_existing_managers_then_alter_managers_variant_2(self):
    """
    A CreateModel that already has managers should be replaced by
    the AlterModelManagers operation when optimized.
    """
    original_managers = [('objects', EmptyManager()), ('old', models.Manager())]
    new_managers = [('objects', models.Manager()), ('new', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[], managers=original_managers), migrations.AlterModelManagers(name='Foo', managers=new_managers)], [migrations.CreateModel('Foo', fields=[], managers=new_managers)])

def test_create_alter_managers_and_add_field_variant_3(self):
    """
    CreateModel + AlterModelManagers + AddField => single CreateModel
    including the added field and new managers.
    """
    managers = [('objects', models.Manager()), ('m', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', [('a', models.IntegerField())]), migrations.AlterModelManagers(name='Foo', managers=managers), migrations.AddField('Foo', 'b', models.IntegerField())], [migrations.CreateModel('Foo', [('a', models.IntegerField()), ('b', models.IntegerField())], managers=managers)])

def test_create_alter_managers_and_alter_field_variant_4(self):
    """
    CreateModel + AlterModelManagers + AlterField => single CreateModel with
    the altered field and new managers.
    """
    managers = [('objects', models.Manager()), ('m', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', [('x', models.CharField(max_length=10))]), migrations.AlterModelManagers(name='Foo', managers=managers), migrations.AlterField('Foo', 'x', models.IntegerField())], [migrations.CreateModel('Foo', [('x', models.IntegerField())], managers=managers)])

def test_create_alter_managers_and_remove_field_variant_5(self):
    """
    CreateModel + AlterModelManagers + RemoveField => single CreateModel with
    the field removed and new managers applied.
    """
    managers = [('objects', models.Manager()), ('m', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', [('a', models.IntegerField()), ('b', models.IntegerField())]), migrations.AlterModelManagers(name='Foo', managers=managers), migrations.RemoveField('Foo', 'b')], [migrations.CreateModel('Foo', [('a', models.IntegerField())], managers=managers)])

def test_create_alter_managers_and_rename_field_variant_6(self):
    """
    CreateModel + AlterModelManagers + RenameField => single CreateModel with
    the field renamed and managers replaced.
    """
    managers = [('objects', models.Manager()), ('m', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', [('a', models.IntegerField()), ('b', models.IntegerField())]), migrations.AlterModelManagers(name='Foo', managers=managers), migrations.RenameField('Foo', 'b', 'c')], [migrations.CreateModel('Foo', [('a', models.IntegerField()), ('c', models.IntegerField())], managers=managers)])

def test_create_alter_managers_and_alter_model_options_variant_7(self):
    """
    CreateModel + AlterModelManagers + AlterModelOptions => CreateModel should
    contain the updated options and the new managers.
    """
    managers = [('objects', models.Manager()), ('m', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[], options={'verbose_name': 'F'}), migrations.AlterModelManagers(name='Foo', managers=managers), migrations.AlterModelOptions(name='Foo', options={'verbose_name_plural': 'Fs'})], [migrations.CreateModel('Foo', fields=[], options={'verbose_name_plural': 'Fs'}, managers=managers)])

def test_create_alter_managers_and_rename_model_variant_8(self):
    """
    CreateModel + AlterModelManagers + RenameModel should produce a single
    CreateModel with the new name and the updated managers.
    """
    managers = [('objects', models.Manager()), ('m', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', [('x', models.IntegerField())]), migrations.AlterModelManagers(name='Foo', managers=managers), migrations.RenameModel('Foo', 'Bar')], [migrations.CreateModel('Bar', [('x', models.IntegerField())], managers=managers)])

def test_alter_managers_for_different_model_does_not_optimize_variant_9(self):
    """
    AlterModelManagers targeting a different model should not change the
    CreateModel for another model.
    """
    managers = [('objects', models.Manager()), ('m', EmptyManager())]
    self.assertDoesNotOptimize([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Bar', managers=managers)])

def test_create_alter_managers_then_delete_model_variant_10(self):
    """
    CreateModel + AlterModelManagers + DeleteModel should collapse into no
    operations (Create then Delete of same model).
    """
    managers = [('objects', models.Manager()), ('m', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', [('a', models.IntegerField())]), migrations.AlterModelManagers(name='Foo', managers=managers), migrations.DeleteModel('Foo')], [])

from django.db import models, migrations
from .models import EmptyManager, UnicodeModel
from django.db.migrations import operations

def test_create_model_addfield_then_alter_managers(self):
    """
    CreateModel + AddField + AlterModelManagers should collapse to a single
    CreateModel with the new field and new managers.
    """
    ops = [migrations.CreateModel('Foo', [('name', models.CharField(max_length=255))]), migrations.AddField('Foo', 'age', models.IntegerField()), migrations.AlterModelManagers(name='Foo', managers=[('objects', models.Manager()), ('things', EmptyManager())])]
    expected = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=255)), ('age', models.IntegerField())], managers=[('objects', models.Manager()), ('things', EmptyManager())])]
    self.assertOptimizesTo(ops, expected)

def test_create_model_alter_managers_then_addfield(self):
    """
    CreateModel + AlterModelManagers + AddField should also collapse to a single
    CreateModel with both managers and field present.
    """
    ops = [migrations.CreateModel('Foo', [('name', models.CharField(max_length=255))]), migrations.AlterModelManagers(name='Foo', managers=[('objects', models.Manager()), ('active_only', EmptyManager())]), migrations.AddField('Foo', 'active', models.BooleanField(default=True))]
    expected = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=255)), ('active', models.BooleanField(default=True))], managers=[('objects', models.Manager()), ('active_only', EmptyManager())])]
    self.assertOptimizesTo(ops, expected)

def test_create_model_alterfield_and_alter_managers(self):
    """
    CreateModel + AlterField + AlterModelManagers should collapse to CreateModel
    with the field type updated and managers replaced.
    """
    managers = [('objects', models.Manager()), ('m', EmptyManager())]
    ops = [migrations.CreateModel(name='Foo', fields=[('name', models.CharField(max_length=255))]), migrations.AlterField('Foo', 'name', models.TextField()), migrations.AlterModelManagers(name='Foo', managers=managers)]
    expected = [migrations.CreateModel(name='Foo', fields=[('name', models.TextField())], managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_model_removefield_and_alter_managers(self):
    """
    CreateModel with two fields + RemoveField + AlterModelManagers should
    produce a single CreateModel with only the remaining field and managers.
    """
    managers = [('objects', models.Manager()), ('mgr', EmptyManager())]
    ops = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=255)), ('age', models.IntegerField())]), migrations.RemoveField('Foo', 'age'), migrations.AlterModelManagers(name='Foo', managers=managers)]
    expected = [migrations.CreateModel('Foo', fields=[('name', models.CharField(max_length=255))], managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_model_renamefield_and_alter_managers(self):
    """
    CreateModel + RenameField + AlterModelManagers should collapse into
    CreateModel with the renamed field and new managers.
    """
    managers = [('objects', models.Manager()), ('custom', EmptyManager())]
    ops = [migrations.CreateModel('Foo', fields=[('title', models.CharField(max_length=50))]), migrations.RenameField('Foo', 'title', 'heading'), migrations.AlterModelManagers(name='Foo', managers=managers)]
    expected = [migrations.CreateModel('Foo', fields=[('heading', models.CharField(max_length=50))], managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_model_alter_unique_together_and_alter_managers(self):
    """
    CreateModel + AlterUniqueTogether + AlterModelManagers should result in
    a CreateModel that contains both the unique_together option and the new managers.
    """
    managers = [('objects', models.Manager()), ('mm', EmptyManager())]
    ops = [migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())]), migrations.AlterUniqueTogether('Foo', [['a', 'b']]), migrations.AlterModelManagers(name='Foo', managers=managers)]
    expected = [migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())], options={'unique_together': {('a', 'b')}}, managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_model_alter_index_together_and_alter_managers(self):
    """
    Same as unique_together but for index_together.
    """
    managers = [('objects', models.Manager()), ('mm', EmptyManager())]
    ops = [migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())]), migrations.AlterIndexTogether('Foo', [['a', 'b']]), migrations.AlterModelManagers(name='Foo', managers=managers)]
    expected = [migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())], options={'index_together': {('a', 'b')}}, managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_model_alter_owrt_and_alter_managers(self):
    """
    AlterOrderWithRespectTo and AlterModelManagers together should produce a
    CreateModel with order_with_respect_to set and managers replaced.
    """
    managers = [('objects', models.Manager()), ('mm', EmptyManager())]
    ops = [migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())]), migrations.AlterOrderWithRespectTo('Foo', 'a'), migrations.AlterModelManagers(name='Foo', managers=managers)]
    expected = [migrations.CreateModel('Foo', fields=[('a', models.IntegerField()), ('b', models.IntegerField())], options={'order_with_respect_to': 'a'}, managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_model_alter_model_options_and_alter_managers(self):
    """
    CreateModel + AlterModelOptions + AlterModelManagers should collapse into
    a single CreateModel that contains both the updated options and the
    updated managers.
    """
    managers = [('objects', models.Manager()), ('custom', EmptyManager())]
    ops = [migrations.CreateModel('Foo', fields=[]), migrations.AlterModelOptions(name='Foo', options={'verbose_name': 'Bar'}), migrations.AlterModelManagers(name='Foo', managers=managers)]
    expected = [migrations.CreateModel('Foo', fields=[], options={'verbose_name': 'Bar'}, managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_model_replace_managers_only(self):
    """
    If AlterModelManagers replaces the managers, the result should have only
    the new managers (not a merge with the original).
    """
    ops = [migrations.CreateModel('Foo', fields=[], managers=[('objects', models.Manager())]), migrations.AlterModelManagers(name='Foo', managers=[('new', EmptyManager())])]
    expected = [migrations.CreateModel('Foo', fields=[], managers=[('new', EmptyManager())])]
    self.assertOptimizesTo(ops, expected)
from tests.migrations.test_optimizer import OptimizerTests as _OT
_OT.test_create_model_addfield_then_alter_managers = test_create_model_addfield_then_alter_managers
_OT.test_create_model_alter_managers_then_addfield = test_create_model_alter_managers_then_addfield
_OT.test_create_model_alterfield_and_alter_managers = test_create_model_alterfield_and_alter_managers
_OT.test_create_model_removefield_and_alter_managers = test_create_model_removefield_and_alter_managers
_OT.test_create_model_renamefield_and_alter_managers = test_create_model_renamefield_and_alter_managers
_OT.test_create_model_alter_unique_together_and_alter_managers = test_create_model_alter_unique_together_and_alter_managers
_OT.test_create_model_alter_index_together_and_alter_managers = test_create_model_alter_index_together_and_alter_managers
_OT.test_create_model_alter_owrt_and_alter_managers = test_create_model_alter_owrt_and_alter_managers
_OT.test_create_model_alter_model_options_and_alter_managers = test_create_model_alter_model_options_and_alter_managers
_OT.test_create_model_replace_managers_only = test_create_model_replace_managers_only

def test_create_alter_model_managers_simple_extra(self):
    managers = [('objects', models.Manager()), ('things', EmptyManager())]
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=managers)], [migrations.CreateModel('Foo', fields=[], managers=managers)])

def test_create_then_alter_managers_then_add_field(self):
    managers = [('objects', models.Manager()), ('custom', EmptyManager())]
    ops = [migrations.CreateModel('Alpha', fields=[]), migrations.AlterModelManagers(name='Alpha', managers=managers), migrations.AddField('Alpha', 'count', models.IntegerField())]
    expected = [migrations.CreateModel('Alpha', fields=[('count', models.IntegerField())], managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_add_field_then_alter_managers(self):
    managers = [('objects', models.Manager()), ('custom', EmptyManager())]
    ops = [migrations.CreateModel('Beta', fields=[]), migrations.AddField('Beta', 'score', models.FloatField(default=0.0)), migrations.AlterModelManagers(name='Beta', managers=managers)]
    expected = [migrations.CreateModel('Beta', fields=[('score', models.FloatField(default=0.0))], managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_preserves_bases_and_options_when_altering_managers(self):
    managers = [('objects', models.Manager()), ('em', EmptyManager())]
    ops = [migrations.CreateModel(name='Gamma', fields=[('name', models.CharField(max_length=50))], options={'verbose_name': 'G'}, bases=('migrations.UnicodeModel',), managers=[('objects', models.Manager())]), migrations.AlterModelManagers(name='Gamma', managers=managers)]
    expected = [migrations.CreateModel(name='Gamma', fields=[('name', models.CharField(max_length=50))], options={'verbose_name': 'G'}, bases=('migrations.UnicodeModel',), managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_managers_case_insensitive(self):
    managers = [('objects', models.Manager()), ('custom', EmptyManager())]
    ops = [migrations.CreateModel('MiXeDCase', fields=[('a', models.IntegerField())]), migrations.AlterModelManagers(name='mixedcase', managers=managers)]
    expected = [migrations.CreateModel('MiXeDCase', fields=[('a', models.IntegerField())], managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_managers_for_different_model_no_opt(self):
    managers = [('objects', models.Manager()), ('x', EmptyManager())]
    ops = [migrations.CreateModel('Delta', fields=[]), migrations.AlterModelManagers(name='Other', managers=managers)]
    self.assertOptimizesTo(ops, ops)

def test_create_rename_field_then_alter_managers(self):
    managers = [('objects', models.Manager()), ('custom', EmptyManager())]
    ops = [migrations.CreateModel('Epsilon', fields=[('old', models.CharField(max_length=20))]), migrations.RenameField('Epsilon', 'old', 'new'), migrations.AlterModelManagers(name='Epsilon', managers=managers)]
    expected = [migrations.CreateModel('Epsilon', fields=[('new', models.CharField(max_length=20))], managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_multiple_alter_model_managers_sequence(self):
    m1 = [('objects', models.Manager()), ('a', EmptyManager())]
    m2 = [('objects', models.Manager()), ('b', EmptyManager())]
    ops = [migrations.CreateModel('Zeta', fields=[]), migrations.AlterModelManagers(name='Zeta', managers=m1), migrations.AlterModelManagers(name='Zeta', managers=m2)]
    expected = [migrations.CreateModel('Zeta', fields=[], managers=m2)]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_managers_and_alter_options(self):
    managers = [('objects', models.Manager()), ('mgr', EmptyManager())]
    ops = [migrations.CreateModel('Theta', fields=[('x', models.IntegerField())]), migrations.AlterModelManagers(name='Theta', managers=managers), migrations.AlterModelOptions(name='Theta', options={'verbose_name': 'T'})]
    expected = [migrations.CreateModel('Theta', fields=[('x', models.IntegerField())], options={'verbose_name': 'T'}, managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_managers_among_unrelated_ops(self):
    managers = [('objects', models.Manager()), ('m', EmptyManager())]
    ops = [migrations.CreateModel('Keep', fields=[('f', models.TextField())]), migrations.CreateModel('Tmp', fields=[('t', models.IntegerField())]), migrations.AlterModelManagers(name='Keep', managers=managers), migrations.DeleteModel('Tmp')]
    expected = [migrations.CreateModel('Keep', fields=[('f', models.TextField())], managers=managers)]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_model_managers_case_insensitive(self):
    """
    The optimizer should treat model names case-insensitively when merging
    CreateModel and AlterModelManagers.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='foo', managers=[('a', EmptyManager()), ('b', models.Manager())])], [migrations.CreateModel('Foo', fields=[], managers=[('a', EmptyManager()), ('b', models.Manager())])])

def test_create_without_managers_then_alter_sets_managers(self):
    """
    A CreateModel without explicit managers should be merged with an
    AlterModelManagers that sets managers.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('custom', EmptyManager())])], [migrations.CreateModel('Foo', fields=[], managers=[('custom', EmptyManager())])])

def test_create_with_default_managers_then_alter(self):
    """
    If CreateModel explicitly declares the default manager list, it should
    still be overwritten by AlterModelManagers.
    """
    self.assertOptimizesTo([migrations.CreateModel(name='Foo', fields=[], managers=[('objects', models.Manager())]), migrations.AlterModelManagers(name='Foo', managers=[('things', EmptyManager())])], [migrations.CreateModel('Foo', fields=[], managers=[('things', EmptyManager())])])

def test_create_with_existing_managers_overwritten(self):
    """
    Existing managers on CreateModel should be replaced by AlterModelManagers.
    """
    self.assertOptimizesTo([migrations.CreateModel(name='Foo', fields=[], managers=[('objects', EmptyManager()), ('x', models.Manager())]), migrations.AlterModelManagers(name='Foo', managers=[('new', EmptyManager())])], [migrations.CreateModel('Foo', fields=[], managers=[('new', EmptyManager())])])

def test_create_then_two_alter_managers_last_wins(self):
    """
    Multiple AlterModelManagers after a CreateModel should result in a single
    CreateModel with the managers from the last AlterModelManagers.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('a', EmptyManager())]), migrations.AlterModelManagers(name='Foo', managers=[('b', models.Manager())])], [migrations.CreateModel('Foo', fields=[], managers=[('b', models.Manager())])])

def test_create_then_alter_managers_other_model_not_merged(self):
    """
    AlterModelManagers for a different model should not be merged into the
    CreateModel.
    """
    ops = [migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers('Bar', managers=[('x', EmptyManager())])]
    self.assertDoesNotOptimize(ops)

def test_create_then_alter_and_addfield(self):
    """
    CreateModel followed by AlterModelManagers and then AddField should
    optimize into a single CreateModel containing both the new manager(s)
    and the added field.
    """
    ops = [migrations.CreateModel(name='Foo', fields=[('name', models.CharField(max_length=50))]), migrations.AlterModelManagers(name='Foo', managers=[('custom', EmptyManager())]), migrations.AddField('Foo', 'age', models.IntegerField())]
    self.assertOptimizesTo(ops, [migrations.CreateModel(name='Foo', fields=[('name', models.CharField(max_length=50)), ('age', models.IntegerField())], managers=[('custom', EmptyManager())])])

def test_create_then_alter_managers_empty_list(self):
    """
    AlterModelManagers that sets an empty list of managers should result in
    a CreateModel that has an explicit empty managers list.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[])], [migrations.CreateModel('Foo', fields=[], managers=[])])

def test_create_alter_preserve_options(self):
    """
    AlterModelManagers should not affect other CreateModel attributes like
    options; options should be preserved.
    """
    self.assertOptimizesTo([migrations.CreateModel('Foo', fields=[], options={'verbose_name': 'Thing'}), migrations.AlterModelManagers(name='Foo', managers=[('m', EmptyManager())])], [migrations.CreateModel('Foo', fields=[], options={'verbose_name': 'Thing'}, managers=[('m', EmptyManager())])])

def test_create_alter_managers_default_equivalence(self):
    """
    If AlterModelManagers sets the default list of managers
    ([('objects', models.Manager())]) and CreateModel omitted managers (uses
    default), the optimized output should be a single CreateModel with no
    explicit managers (serialization omits the default).
    """
    ops = [migrations.CreateModel('Foo', fields=[]), migrations.AlterModelManagers(name='Foo', managers=[('objects', models.Manager())])]
    self.assertOptimizesTo(ops, [migrations.CreateModel('Foo', fields=[])])

def test_create_addfield_then_alter_managers(self):
    """
    CreateModel + AddField + AlterModelManagers should optimize into a single
    CreateModel that has both the added field and the new managers.
    """
    managers_initial = [('objects', EmptyManager())]
    create = migrations.CreateModel('Foo', [('a', models.IntegerField())], managers=managers_initial)
    add = migrations.AddField('Foo', 'b', models.IntegerField())
    managers_new = [('objects', EmptyManager()), ('m2', EmptyManager())]
    alter_managers = migrations.AlterModelManagers('Foo', managers=managers_new)
    self.assertOptimizesTo([create, add, alter_managers], [migrations.CreateModel('Foo', [('a', models.IntegerField()), ('b', models.IntegerField())], managers=managers_new)])

def test_create_alter_managers_then_addfield(self):
    """
    CreateModel + AlterModelManagers + AddField (managers before add) should
    still optimize into a single CreateModel with both the field and managers.
    """
    managers_initial = [('objects', EmptyManager())]
    create = migrations.CreateModel('Foo', [('a', models.IntegerField())], managers=managers_initial)
    managers_new = [('objects', EmptyManager()), ('m2', EmptyManager())]
    alter_managers = migrations.AlterModelManagers('Foo', managers=managers_new)
    add = migrations.AddField('Foo', 'b', models.IntegerField())
    self.assertOptimizesTo([create, alter_managers, add], [migrations.CreateModel('Foo', [('a', models.IntegerField()), ('b', models.IntegerField())], managers=managers_new)])

def test_create_renamefield_then_alter_managers(self):
    """
    RenameField followed by AlterModelManagers should result in CreateModel
    with the renamed field and new managers.
    """
    managers_initial = [('objects', EmptyManager())]
    create = migrations.CreateModel('Foo', [('name', models.CharField(max_length=10))], managers=managers_initial)
    rename = migrations.RenameField('Foo', 'name', 'title')
    managers_new = [('objects', EmptyManager()), ('m2', EmptyManager())]
    alter_managers = migrations.AlterModelManagers('Foo', managers=managers_new)
    self.assertOptimizesTo([create, rename, alter_managers], [migrations.CreateModel('Foo', [('title', models.CharField(max_length=10))], managers=managers_new)])

def test_create_removefield_then_alter_managers(self):
    """
    RemoveField (removing an existing field) then AlterModelManagers should
    produce CreateModel without the removed field and with new managers.
    """
    managers_initial = [('objects', EmptyManager())]
    create = migrations.CreateModel('Foo', [('name', models.CharField(max_length=10)), ('age', models.IntegerField())], managers=managers_initial)
    remove = migrations.RemoveField('Foo', 'age')
    managers_new = [('objects', EmptyManager()), ('m2', EmptyManager())]
    alter_managers = migrations.AlterModelManagers('Foo', managers=managers_new)
    self.assertOptimizesTo([create, remove, alter_managers], [migrations.CreateModel('Foo', [('name', models.CharField(max_length=10))], managers=managers_new)])

def test_alter_managers_name_case_insensitive(self):
    """
    AlterModelManagers with different-cased model name should still be
    absorbed into CreateModel (case-insensitive matching).
    """
    managers_initial = [('objects', EmptyManager())]
    create = migrations.CreateModel('Foo', [], managers=managers_initial)
    managers_new = [('new', EmptyManager())]
    alter_managers = migrations.AlterModelManagers('foo', managers=managers_new)
    self.assertOptimizesTo([create, alter_managers], [migrations.CreateModel('Foo', [], managers=managers_new)])

def test_create_alter_options_and_managers(self):
    """
    CreateModel + AlterModelOptions + AlterModelManagers should collapse into
    a single CreateModel that has both the options and the managers applied.
    """
    managers_initial = [('objects', EmptyManager())]
    create = migrations.CreateModel('Foo', [], managers=managers_initial)
    alter_options = migrations.AlterModelOptions('Foo', options={'verbose_name': 'X'})
    managers_new = [('xman', EmptyManager())]
    alter_managers = migrations.AlterModelManagers('Foo', managers=managers_new)
    self.assertOptimizesTo([create, alter_options, alter_managers], [migrations.CreateModel('Foo', [], options={'verbose_name': 'X'}, managers=managers_new)])

def test_create_addfield_alter_options_alter_managers(self):
    """
    CreateModel + AddField + AlterModelOptions + AlterModelManagers should
    become a single CreateModel with the new field, options and managers.
    """
    managers_initial = [('objects', EmptyManager())]
    create = migrations.CreateModel('Foo', [('a', models.IntegerField())], managers=managers_initial)
    add = migrations.AddField('Foo', 'b', models.IntegerField())
    alter_options = migrations.AlterModelOptions('Foo', options={'ordering': ['a']})
    managers_new = [('mgr', EmptyManager())]
    alter_managers = migrations.AlterModelManagers('Foo', managers=managers_new)
    self.assertOptimizesTo([create, add, alter_options, alter_managers], [migrations.CreateModel('Foo', [('a', models.IntegerField()), ('b', models.IntegerField())], options={'ordering': ['a']}, managers=managers_new)])

def test_create_alter_managers_then_delete_model_collapses(self):
    """
    CreateModel + AlterModelManagers + DeleteModel should collapse to nothing.
    """
    create = migrations.CreateModel('Foo', [])
    alter_managers = migrations.AlterModelManagers('Foo', managers=[('m', EmptyManager())])
    delete = migrations.DeleteModel('Foo')
    self.assertOptimizesTo([create, alter_managers, delete], [])

def test_create_addfield_alter_managers_then_delete_model_collapses(self):
    """
    CreateModel + AddField + AlterModelManagers + DeleteModel should collapse
    to nothing (all changes are elidable).
    """
    create = migrations.CreateModel('Foo', [('a', models.IntegerField())])
    add = migrations.AddField('Foo', 'b', models.IntegerField())
    alter_managers = migrations.AlterModelManagers('Foo', managers=[('m', EmptyManager())])
    delete = migrations.DeleteModel('Foo')
    self.assertOptimizesTo([create, add, alter_managers, delete], [])

def test_alter_managers_replaces_rather_than_appends(self):
    """
    AlterModelManagers should replace the CreateModel.managers rather than
    appending to them.
    """
    managers_initial = [('objects', EmptyManager())]
    create = migrations.CreateModel('Foo', [], managers=managers_initial)
    managers_new = [('only', EmptyManager())]
    alter_managers = migrations.AlterModelManagers('Foo', managers=managers_new)
    self.assertOptimizesTo([create, alter_managers], [migrations.CreateModel('Foo', [], managers=managers_new)])