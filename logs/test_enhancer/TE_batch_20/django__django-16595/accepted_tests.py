def test_regression_alter_alter_field_custom_app_label(self):
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256)), migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    self.assertOptimizesTo(ops, expected, app_label='books')

def test_regression_three_alterfields_collapses_to_last_custom_app_label(self):
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256)), migrations.AlterField('Book', 'title', models.CharField(max_length=200, help_text='h1')), migrations.AlterField('Book', 'title', models.CharField(max_length=128, help_text='h2'))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=128, help_text='h2'))]
    self.assertOptimizesTo(ops, expected, app_label='books')

def test_regression_alterfields_preserve_default_false_collapses(self):
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256), preserve_default=False), migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    self.assertOptimizesTo(ops, expected, app_label='books')

def test_regression_alterfields_case_insensitive_names_collapse(self):
    ops = [migrations.AlterField('BOOK', 'TITLE', models.CharField(max_length=50)), migrations.AlterField('book', 'title', models.CharField(max_length=40))]
    expected = [migrations.AlterField('book', 'title', models.CharField(max_length=40))]
    self.assertOptimizesTo(ops, expected, app_label='books')

def test_regression_alterfields_with_different_defaults_keep_last(self):
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=10, default='a')), migrations.AlterField('Book', 'title', models.CharField(max_length=20, default='b'))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=20, default='b'))]
    self.assertOptimizesTo(ops, expected, app_label='books')

def test_regression_alterfields_different_models_do_not_collapse(self):
    ops = [migrations.AlterField('Foo', 'name', models.IntegerField()), migrations.AlterField('Bar', 'name', models.IntegerField())]
    self.assertDoesNotOptimize(ops, app_label='books')

def test_regression_alterfields_different_names_do_not_collapse(self):
    ops = [migrations.AlterField('Book', 'a', models.IntegerField()), migrations.AlterField('Book', 'b', models.IntegerField())]
    self.assertDoesNotOptimize(ops, app_label='books')

def test_regression_alter_then_rename_moves_alter_to_new_name_when_db_column_none(self):
    ops = [migrations.AlterField('Foo', 'name', models.CharField(max_length=255)), migrations.RenameField('Foo', 'name', 'title'), migrations.RenameField('Foo', 'title', 'nom')]
    expected = [migrations.RenameField('Foo', 'name', 'nom'), migrations.AlterField('Foo', 'nom', models.CharField(max_length=255))]
    self.assertOptimizesTo(ops, expected, app_label='books')

def test_regression_multiple_alterfields_with_help_and_default_collapses(self):
    ops = [migrations.AlterField('Book', 'summary', models.CharField(max_length=300, help_text='first', default=None)), migrations.AlterField('Book', 'summary', models.CharField(max_length=200, help_text='second', default='x')), migrations.AlterField('Book', 'summary', models.CharField(max_length=150, help_text='final', default=None))]
    expected = [migrations.AlterField('Book', 'summary', models.CharField(max_length=150, help_text='final', default=None))]
    self.assertOptimizesTo(ops, expected, app_label='books')

def test_regression_three_alterfields_mixed_case_and_preserve_default(self):
    ops = [migrations.AlterField('MyModel', 'Field', models.CharField(max_length=100), preserve_default=False), migrations.AlterField('mymodel', 'field', models.CharField(max_length=90, help_text='a')), migrations.AlterField('MYMODEL', 'FIELD', models.CharField(max_length=80, help_text='b'))]
    expected = [migrations.AlterField('MYMODEL', 'FIELD', models.CharField(max_length=80, help_text='b'))]
    self.assertOptimizesTo(ops, expected, app_label='books')

def test_regression_alter_alter_collapses_simple(self):
    """Two consecutive AlterField operations on the same field should collapse to the latter."""
    self.assertOptimizesTo([migrations.AlterField('Book', 'title', models.CharField(max_length=256)), migrations.AlterField('Book', 'title', models.CharField(max_length=128))], [migrations.AlterField('Book', 'title', models.CharField(max_length=128))])

def test_regression_alter_alter_case_insensitive(self):
    """Model and field name comparisons should be case-insensitive when collapsing AlterField ops."""
    self.assertOptimizesTo([migrations.AlterField('Book', 'Title', models.CharField(max_length=256)), migrations.AlterField('book', 'title', models.CharField(max_length=128))], [migrations.AlterField('book', 'title', models.CharField(max_length=128))])

def test_regression_alter_alter_different_field_no_collapse(self):
    """AlterField operations on different fields must not be collapsed."""
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256)), migrations.AlterField('Book', 'subtitle', models.CharField(max_length=128))]
    self.assertDoesNotOptimize(ops)

def test_regression_alter_alter_chain_collapses_to_last(self):
    """A chain of three AlterField operations on the same field should collapse to the last one."""
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=300)), migrations.AlterField('Book', 'title', models.CharField(max_length=256)), migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    self.assertOptimizesTo(ops, expected)

def test_regression_alterfields_only_subsequence_optimized(self):
    """Optimizing a list consisting only of AlterField operations should collapse them to the final AlterField."""
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=300)), migrations.AlterField('Book', 'title', models.CharField(max_length=200))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=200))]
    self.assertOptimizesTo(ops, expected, app_label='books')

def test_regression_alter_and_rename_field_db_column_none(self):
    """When an AlterField is followed by a RenameField and the AlterField.field.db_column is None, the rename should come first and the alter should apply to the new name."""
    field = models.CharField(max_length=255)
    ops = [migrations.AlterField('Foo', 'name', field), migrations.RenameField('Foo', 'name', 'title')]
    expected = [migrations.RenameField('Foo', 'name', 'title'), migrations.AlterField('Foo', 'title', field)]
    self.assertOptimizesTo(ops, expected)

def test_regression_alter_and_rename_field_db_column_not_none(self):
    """When AlterField.field.db_column is not None, the special-case forwarding across RenameField should not occur."""
    field_with_column = models.CharField(max_length=255, db_column='custom_col')
    ops = [migrations.AlterField('Foo', 'name', field_with_column), migrations.RenameField('Foo', 'name', 'title')]
    self.assertDoesNotOptimize(ops)

def test_regression_alterfields_unrelated_model_no_collapse(self):
    """AlterField operations with the same field name but on different models must not be collapsed."""
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=300)), migrations.AlterField('Author', 'title', models.CharField(max_length=200))]
    self.assertDoesNotOptimize(ops)

def test_regression_alter_alter_with_default_changes_collapses(self):
    """AlterField operations that change defaults or other attributes should still collapse to the final AlterField."""
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256, default='A')), migrations.AlterField('Book', 'title', models.CharField(max_length=256, default='B'))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=256, default='B'))]
    self.assertOptimizesTo(ops, expected)

def test_double_alterfield_collapses(self):
    """
    Two consecutive AlterField operations on the same model/field should
    collapse into the latter AlterField.
    """
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256)), migrations.AlterField('Book', 'title', models.CharField(max_length=128, help_text='h'))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=128, help_text='h'))]
    self.assertOptimizesTo(ops, expected, exact=1)

def test_triple_alterfield_collapses_to_last(self):
    """
    Three AlterField operations in a row should collapse to only the last one.
    """
    ops = [migrations.AlterField('Foo', 'bar', models.IntegerField()), migrations.AlterField('Foo', 'bar', models.IntegerField(null=True)), migrations.AlterField('Foo', 'bar', models.IntegerField(null=True, help_text='x'))]
    expected = [migrations.AlterField('Foo', 'bar', models.IntegerField(null=True, help_text='x'))]
    self.assertOptimizesTo(ops, expected)

def test_alterfield_case_insensitive_model_and_field(self):
    """
    Model and field name comparisons are case-insensitive for collapsing.
    """
    ops = [migrations.AlterField('MyModel', 'Name', models.CharField(max_length=100)), migrations.AlterField('mymodel', 'name', models.CharField(max_length=80))]
    expected = [migrations.AlterField('mymodel', 'name', models.CharField(max_length=80))]
    self.assertOptimizesTo(ops, expected)

def test_alterfield_different_models_not_collapsed(self):
    """
    AlterField operations on different models with the same field name should
    not be collapsed.
    """
    ops = [migrations.AlterField('A', 'value', models.IntegerField()), migrations.AlterField('B', 'value', models.IntegerField(null=True))]
    self.assertOptimizesTo(ops, ops)

def test_alterfield_followed_by_rename_with_db_column_none(self):
    """
    If the altered field has db_column is None, a subsequent RenameField
    should result in RenameField followed by an AlterField on the new name.
    """
    field = models.CharField(max_length=50)
    ops = [migrations.AlterField('Shelf', 'label', field), migrations.RenameField('Shelf', 'label', 'title')]
    expected = [migrations.RenameField('Shelf', 'label', 'title'), migrations.AlterField('Shelf', 'title', field)]
    self.assertOptimizesTo(ops, expected)

def test_alterfield_followed_by_rename_with_db_column_not_none(self):
    """
    If the altered field has a custom db_column (non-None), a subsequent
    RenameField should not keep the AlterField (no alter is needed).
    """
    field = models.CharField(max_length=50, db_column='custom_col')
    ops = [migrations.AlterField('Shelf', 'label', field), migrations.RenameField('Shelf', 'label', 'title')]
    expected = [migrations.RenameField('Shelf', 'label', 'title')]
    self.assertOptimizesTo(ops, expected)

def test_alterfield_case_insensitive_field_name(self):
    """
    Field name comparison for collapsing should be case-insensitive.
    """
    ops = [migrations.AlterField('Thing', 'COUNT', models.IntegerField()), migrations.AlterField('Thing', 'count', models.IntegerField(null=True))]
    expected = [migrations.AlterField('Thing', 'count', models.IntegerField(null=True))]
    self.assertOptimizesTo(ops, expected)

def test_alterfield_only_sequence_optimizes(self):
    """
    Optimizing a list containing only AlterField operations should collapse
    them to the final AlterField.
    """
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256)), migrations.AlterField('Book', 'title', models.CharField(max_length=128)), migrations.AlterField('Book', 'title', models.CharField(max_length=64))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=64))]
    self.assertOptimizesTo(ops, expected)

def test_alterfield_and_other_model_same_field_name(self):
    """
    Ensure that an AlterField for one model and an AlterField for another model
    with the same field name are not collapsed even with case differences.
    """
    ops = [migrations.AlterField('Alpha', 'x', models.IntegerField()), migrations.AlterField('alpha2', 'X', models.IntegerField(null=True))]
    self.assertOptimizesTo(ops, ops)

def test_three_consecutive_alterfields_collapsed(self):
    """
    Three consecutive AlterField operations on the same model/field should
    collapse to a single AlterField (the last one).
    """
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256, null=True)), migrations.AlterField('Book', 'title', models.CharField(max_length=128, null=True)), migrations.AlterField('Book', 'title', models.CharField(max_length=128, null=True, help_text='help'))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=128, null=True, help_text='help'))]
    self.assertOptimizesTo(ops, expected, app_label='books')

def test_three_alterfields_with_default_change_collapsed(self):
    """
    A chain of AlterField operations where the final one changes the default
    should collapse to the final AlterField that contains the default.
    """
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256, null=True)), migrations.AlterField('Book', 'title', models.CharField(max_length=128, null=True)), migrations.AlterField('Book', 'title', models.CharField(max_length=128, null=True, default='x'))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=128, null=True, default='x'))]
    self.assertOptimizesTo(ops, expected, app_label='books')

def test_alterfields_case_insensitive_fieldname_collapses(self):
    """
    Field names comparison is case-insensitive; AlterField operations with
    different casing should collapse to the last AlterField.
    """
    ops = [migrations.AlterField('Book', 'Title', models.CharField(max_length=256)), migrations.AlterField('book', 'title', models.CharField(max_length=128)), migrations.AlterField('BOOK', 'TITLE', models.CharField(max_length=64))]
    expected = [migrations.AlterField('Book', 'TITLE', models.CharField(max_length=64))]
    self.assertOptimizesTo(ops, expected, app_label='books')

def test_alterfields_case_insensitive_modelname_collapses(self):
    """
    Model names comparison is case-insensitive; AlterField operations with
    different model name casing should collapse to the last AlterField.
    """
    ops = [migrations.AlterField('Book', 'name', models.IntegerField()), migrations.AlterField('book', 'name', models.IntegerField(help_text='h'))]
    expected = [migrations.AlterField('Book', 'name', models.IntegerField(help_text='h'))]
    self.assertOptimizesTo(ops, expected, app_label='library')

def test_different_fields_do_not_collapse(self):
    """
    AlterField operations for different fields should remain unchanged.
    """
    ops = [migrations.AlterField('Foo', 'a', models.IntegerField()), migrations.AlterField('Foo', 'b', models.IntegerField())]
    self.assertDoesNotOptimize(ops)

def test_remove_then_alter_keeps_remove(self):
    """
    A RemoveField followed by an AlterField on the same field should result
    in only the RemoveField.
    """
    ops = [migrations.RemoveField('Foo', 'age'), migrations.AlterField('Foo', 'age', models.IntegerField())]
    expected = [migrations.RemoveField('Foo', 'age')]
    self.assertOptimizesTo(ops, expected)

def test_alter_then_remove_keeps_remove(self):
    """
    An AlterField followed by a RemoveField on the same field should result
    in only the RemoveField (the RemoveField absorbs the earlier AlterField).
    """
    ops = [migrations.AlterField('Foo', 'age', models.IntegerField()), migrations.RemoveField('Foo', 'age')]
    expected = [migrations.RemoveField('Foo', 'age')]
    self.assertOptimizesTo(ops, expected)

def test_nonconsecutive_alterfields_preserve_unrelated(self):
    """
    When AlterField for A, then AlterField for B, then AlterField for A again,
    the final result should keep the (latest) AlterField for B and the latest
    AlterField for A.
    """
    ops = [migrations.AlterField('Foo', 'a', models.IntegerField(max_length=10)), migrations.AlterField('Foo', 'b', models.IntegerField(max_length=20)), migrations.AlterField('Foo', 'a', models.IntegerField(max_length=5))]
    expected = [migrations.AlterField('Foo', 'b', models.IntegerField(max_length=20)), migrations.AlterField('Foo', 'a', models.IntegerField(max_length=5))]
    self.assertOptimizesTo(ops, expected)

def test_multiple_alterfields_on_same_field_optimizes_quickly(self):
    """
    A sequence of multiple AlterField operations on the same field should
    collapse to the last AlterField and the optimizer should converge in a
    small number of iterations.
    """
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=500)), migrations.AlterField('Book', 'title', models.CharField(max_length=400)), migrations.AlterField('Book', 'title', models.CharField(max_length=300)), migrations.AlterField('Book', 'title', models.CharField(max_length=200))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=200))]
    self.assertOptimizesTo(ops, expected, less_than=10, app_label='books')

def test_multiple_alterfields_collapsed(self):
    """
    Multiple successive AlterField operations on the same model/field
    should collapse to only the last AlterField.
    """
    self.assertOptimizesTo([migrations.AlterField('Book', 'title', models.CharField(max_length=256, null=True)), migrations.AlterField('Book', 'title', models.CharField(max_length=128, null=True)), migrations.AlterField('Book', 'title', models.CharField(max_length=128, null=True, help_text='help'))], [migrations.AlterField('Book', 'title', models.CharField(max_length=128, null=True, help_text='help'))])

def test_alterfields_only_optimize(self):
    """
    Optimizing a list composed only of AlterField operations should
    reduce to only the final AlterField.
    """
    operations = [migrations.AlterField('Books', 'name', models.CharField(max_length=200, null=True)), migrations.AlterField('Books', 'name', models.CharField(max_length=100, null=True)), migrations.AlterField('Books', 'name', models.CharField(max_length=50, null=True, help_text='x'))]
    expected = [migrations.AlterField('Books', 'name', models.CharField(max_length=50, null=True, help_text='x'))]
    self.assertOptimizesTo(operations, expected)

def test_alterfields_case_insensitive_fieldnames(self):
    """
    Field/name and model name matching should be case-insensitive when
    deciding whether to collapse AlterField operations.
    """
    ops = [migrations.AlterField('Book', 'Title', models.CharField(max_length=255)), migrations.AlterField('book', 'title', models.CharField(max_length=128))]
    self.assertOptimizesTo(ops, [ops[1]])

def test_addfield_then_multiple_alterfields_becomes_single_addfield(self):
    """
    An AddField followed by several AlterField operations on the same
    field should optimize into a single AddField with the final field.
    """
    ops = [migrations.AddField('Foo', 'age', models.IntegerField()), migrations.AlterField('Foo', 'age', models.FloatField(default=1.2)), migrations.AlterField('Foo', 'age', models.FloatField(default=2.4))]
    expected = [migrations.AddField('Foo', 'age', models.FloatField(default=2.4))]
    self.assertOptimizesTo(ops, expected)

def test_alterfield_then_rename_generates_rename_and_alter(self):
    """
    AlterField followed by RenameField should produce a RenameField and
    an AlterField on the new name when the original field's db_column is None.
    """
    field = models.CharField(max_length=10)
    ops = [migrations.AlterField('App', 'name', field), migrations.RenameField('App', 'name', 'title')]
    expected = [migrations.RenameField('App', 'name', 'title'), migrations.AlterField('App', 'title', field)]
    self.assertOptimizesTo(ops, expected)

def test_multiple_alterfields_followed_by_removefield_results_in_remove(self):
    """
    Several AlterField operations followed by a RemoveField should collapse
    into a single RemoveField operation.
    """
    ops = [migrations.AlterField('X', 'val', models.IntegerField()), migrations.AlterField('X', 'val', models.IntegerField(help_text='h')), migrations.RemoveField('X', 'val')]
    expected = [migrations.RemoveField('X', 'val')]
    self.assertOptimizesTo(ops, expected)

def test_rename_with_db_column_none_keeps_alter_after_rename(self):
    """
    Ensure the special-case that adds an AlterField after a RenameField
    (when db_column is None) still results in the AlterField with the
    original field attributes but the new name.
    """
    original_field = models.TextField()
    ops = [migrations.AlterField('M', 'old', original_field), migrations.RenameField('M', 'old', 'new')]
    expected = [migrations.RenameField('M', 'old', 'new'), migrations.AlterField('M', 'new', original_field)]
    self.assertOptimizesTo(ops, expected)

def test_alterfields_on_different_models_do_not_merge(self):
    """
    AlterField operations on different models must not be merged.
    """
    ops = [migrations.AlterField('A', 'f', models.IntegerField()), migrations.AlterField('B', 'f', models.IntegerField())]
    self.assertOptimizesTo(ops, ops)

def test_modelname_case_insensitive_collapsing(self):
    """
    Model name matching for collapsing AlterField operations should be
    case-insensitive.
    """
    ops = [migrations.AlterField('MyModel', 'x', models.IntegerField()), migrations.AlterField('mymodel', 'x', models.IntegerField(default=5))]
    self.assertOptimizesTo(ops, [ops[1]])

def test_alterfields_with_preserve_default_false_collapsed(self):
    """
    AlterField operations with preserve_default=False should still collapse
    to the last AlterField on the same field.
    """
    ops = [migrations.AlterField('Z', 'num', models.IntegerField(default=1), preserve_default=False), migrations.AlterField('Z', 'num', models.IntegerField(default=2), preserve_default=False)]
    self.assertOptimizesTo(ops, [ops[1]])

from django.test import SimpleTestCase
from django.db import migrations, models
from django.db.migrations import operations
from django.db.migrations.optimizer import MigrationOptimizer
from django.db.migrations.serializer import serializer_factory

def serialize(op):
    return serializer_factory(op).serialize()[0]

def optimize(operations_list, app_label='migrations'):
    optimizer = MigrationOptimizer()
    return optimizer.optimize(operations_list, app_label)

def test_multiple_alterfield_chain_collapses_to_last(self):
    ops = [migrations.AlterField('Foo', 'name', models.CharField(max_length=10)), migrations.AlterField('Foo', 'name', models.CharField(max_length=20)), migrations.AlterField('Foo', 'name', models.CharField(max_length=30))]
    expected = [migrations.AlterField('Foo', 'name', models.CharField(max_length=30))]
    self.assertOptimizesTo(ops, expected)

def test_alterfield_case_insensitive_field_and_model_matching(self):
    ops = [migrations.AlterField('FOO', 'Name', models.CharField(max_length=10)), migrations.AlterField('foo', 'name', models.CharField(max_length=20))]
    expected = [migrations.AlterField('foo', 'name', models.CharField(max_length=20))]
    self.assertOptimizesTo(ops, expected)

def test_alter_then_rename_with_db_column_none_keeps_altered_on_new_name(self):
    field_before = models.CharField(max_length=15)
    ops = [migrations.AlterField('Book', 'title', field_before), migrations.RenameField('Book', 'title', 'headline')]
    expected = [migrations.RenameField('Book', 'title', 'headline'), migrations.AlterField('Book', 'headline', field_before)]
    self.assertOptimizesTo(ops, expected)

def test_alter_then_rename_with_db_column_set_does_not_emit_second_alter(self):
    field_before = models.CharField(max_length=15, db_column='custom_col')
    ops = [migrations.AlterField('Book', 'title', field_before), migrations.RenameField('Book', 'title', 'headline')]
    expected = [migrations.RenameField('Book', 'title', 'headline')]
    self.assertOptimizesTo(ops, expected)

def test_alter_then_rename_then_alter_on_new_name_collapses_properly(self):
    initial = models.CharField(max_length=10)
    middle = models.CharField(max_length=20)
    final = models.CharField(max_length=30)
    ops = [migrations.AlterField('Book', 'title', initial), migrations.RenameField('Book', 'title', 'headline'), migrations.AlterField('Book', 'headline', final)]
    expected = [migrations.RenameField('Book', 'title', 'headline'), migrations.AlterField('Book', 'headline', final)]
    self.assertOptimizesTo(ops, expected)

def test_alterfield_followed_by_removefield_results_in_removefield_only(self):
    ops = [migrations.AlterField('Foo', 'age', models.IntegerField()), migrations.RemoveField('Foo', 'age')]
    expected = [migrations.RemoveField('Foo', 'age')]
    self.assertOptimizesTo(ops, expected)

def test_alterfields_on_different_fields_do_not_collapse(self):
    ops = [migrations.AlterField('Foo', 'a', models.IntegerField()), migrations.AlterField('Foo', 'b', models.IntegerField())]
    self.assertOptimizesTo(ops, ops)

def test_elidable_between_alterfields_does_not_prevent_collapsing(self):
    elidable = operations.base.Operation()
    elidable.elidable = True
    ops = [migrations.AlterField('Foo', 'name', models.CharField(max_length=10)), elidable, migrations.AlterField('Foo', 'name', models.CharField(max_length=50))]
    expected = [migrations.AlterField('Foo', 'name', models.CharField(max_length=50))]
    self.assertOptimizesTo(ops, expected)

def test_chain_of_alterfields_then_rename_then_more_alters_collapses_to_last_alter(self):
    a1 = models.CharField(max_length=5)
    a2 = models.CharField(max_length=6)
    a3 = models.CharField(max_length=7)
    ops = [migrations.AlterField('Book', 'title', a1), migrations.AlterField('Book', 'title', a2), migrations.RenameField('Book', 'title', 'headline'), migrations.AlterField('Book', 'headline', a3)]
    expected = [migrations.RenameField('Book', 'title', 'headline'), migrations.AlterField('Book', 'headline', a3)]
    self.assertOptimizesTo(ops, expected)

def test_multiple_alterfields_chain_with_case_variations_collapses_to_last(self):
    ops = [migrations.AlterField('Book', 'Title', models.CharField(max_length=8)), migrations.AlterField('book', 'title', models.CharField(max_length=9)), migrations.AlterField('BOOK', 'TITLE', models.CharField(max_length=10))]
    expected = [migrations.AlterField('BOOK', 'TITLE', models.CharField(max_length=10))]
    self.assertOptimizesTo(ops, expected)

def test_alter_alter_only_sequence(self):
    """
    Two consecutive AlterField operations on the same field should collapse
    into the latter when the operation list contains only AlterField ops.
    """
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256)), migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    self.assertOptimizesTo(ops, expected)

def test_alter_alter_only_sequence_multiple(self):
    """
    Multiple consecutive AlterField operations on the same field should
    collapse into a single AlterField with the final field state.
    """
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256)), migrations.AlterField('Book', 'title', models.CharField(max_length=192)), migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    self.assertOptimizesTo(ops, expected)

def test_alter_alter_case_insensitive_model_and_name(self):
    """
    Model and field name comparisons are case-insensitive for reduction.
    """
    ops = [migrations.AlterField('Book', 'Title', models.CharField(max_length=256)), migrations.AlterField('book', 'title', models.CharField(max_length=128))]
    expected = [migrations.AlterField('book', 'title', models.CharField(max_length=128))]
    self.assertOptimizesTo(ops, expected)

def test_addfield_then_multiple_alter(self):
    """
    AddField followed by multiple AlterField operations on that field
    should collapse into a single AddField with the final field state.
    """
    ops = [migrations.AddField('Book', 'title', models.CharField(max_length=256)), migrations.AlterField('Book', 'title', models.CharField(max_length=192)), migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    expected = [migrations.AddField('Book', 'title', models.CharField(max_length=128))]
    self.assertOptimizesTo(ops, expected)

def test_alterfield_then_rename_db_column_none(self):
    """
    If an AlterField is followed by a RenameField on the same field and the
    AlterField's field.db_column is None, the optimizer should produce a
    RenameField followed by an AlterField that targets the new name.
    """
    alter_field = models.CharField(max_length=64)
    ops = [migrations.AlterField('Foo', 'name', alter_field), migrations.RenameField('Foo', 'name', 'title')]
    expected = [migrations.RenameField('Foo', 'name', 'title'), migrations.AlterField('Foo', 'title', models.CharField(max_length=64))]
    self.assertOptimizesTo(ops, expected)

def test_alterfield_then_rename_db_column_not_none(self):
    """
    If the AlterField's field.db_column is set (not None), the special-case
    that keeps the AlterField after a RenameField should not apply.
    Only the RenameField should remain.
    """
    alter_field = models.CharField(max_length=64, db_column='legacy_col')
    ops = [migrations.AlterField('Foo', 'name', alter_field), migrations.RenameField('Foo', 'name', 'title')]
    expected = [migrations.RenameField('Foo', 'name', 'title')]
    self.assertOptimizesTo(ops, expected)

def test_alterfields_different_names_not_collapsed(self):
    """
    AlterField operations on different field names should not be collapsed.
    """
    ops = [migrations.AlterField('Foo', 'a', models.CharField(max_length=64)), migrations.AlterField('Foo', 'b', models.CharField(max_length=32))]
    expected = [migrations.AlterField('Foo', 'a', models.CharField(max_length=64)), migrations.AlterField('Foo', 'b', models.CharField(max_length=32))]
    self.assertOptimizesTo(ops, expected)

def test_alterfield_then_removefield(self):
    """
    A RemoveField following an AlterField on the same field should absorb
    the AlterField and result only in a RemoveField.
    """
    ops = [migrations.AlterField('Foo', 'age', models.IntegerField()), migrations.RemoveField('Foo', 'age')]
    expected = [migrations.RemoveField('Foo', 'age')]
    self.assertOptimizesTo(ops, expected)

def test_alterfields_different_models_not_collapsed(self):
    """
    AlterField operations on the same field name but different models should
    not be collapsed.
    """
    ops = [migrations.AlterField('Foo', 'name', models.CharField(max_length=64)), migrations.AlterField('Bar', 'name', models.CharField(max_length=32))]
    expected = [migrations.AlterField('Foo', 'name', models.CharField(max_length=64)), migrations.AlterField('Bar', 'name', models.CharField(max_length=32))]
    self.assertOptimizesTo(ops, expected)

def test_alter_alter_only_sequence_with_app_label(self):
    """
    Two AlterField operations should collapse to one when optimizing with a
    specific app_label provided to the optimizer.
    """
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256)), migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    self.assertOptimizesTo(ops, expected, app_label='customapp')

def test_alter_alter_collapses_to_second(self):
    """
    Two successive AlterField operations on the same model/field collapse
    into the latter AlterField.
    """
    ops = [migrations.AlterField('Book', 'title', models.CharField(max_length=256)), migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    expected = [migrations.AlterField('Book', 'title', models.CharField(max_length=128))]
    self.assertOptimizesTo(ops, expected)

def test_alter_alter_case_insensitive_model_and_field(self):
    """
    AlterField reduction is case-insensitive for model and field names.
    Multiple AlterField ops differing only in case should collapse to the last.
    """
    ops = [migrations.AlterField('BOOK', 'Title', models.CharField(max_length=300)), migrations.AlterField('book', 'title', models.CharField(max_length=100))]
    expected = [migrations.AlterField('book', 'title', models.CharField(max_length=100))]
    self.assertOptimizesTo(ops, expected)

def test_three_alter_field_chain_keeps_last(self):
    """
    A chain of three AlterField operations on the same field collapses to the last.
    """
    ops = [migrations.AlterField('Foo', 'name', models.CharField(max_length=300)), migrations.AlterField('Foo', 'name', models.CharField(max_length=200)), migrations.AlterField('Foo', 'name', models.CharField(max_length=100))]
    expected = [migrations.AlterField('Foo', 'name', models.CharField(max_length=100))]
    self.assertOptimizesTo(ops, expected)

def test_alter_followed_by_single_rename_moves_alter_to_new_name(self):
    """
    AlterField followed by a RenameField (and the field has no db_column)
    should become RenameField + AlterField on the new name.
    """
    field = models.CharField(max_length=64)
    ops = [migrations.AlterField('Book', 'title', field), migrations.RenameField('Book', 'title', 'headline')]
    expected = [migrations.RenameField('Book', 'title', 'headline'), migrations.AlterField('Book', 'headline', models.CharField(max_length=64))]
    self.assertOptimizesTo(ops, expected)

def test_alter_followed_by_rename_with_db_column_set_does_not_move_alter(self):
    """
    If the AlterField's field has db_column set, the optimizer should not move
    the AlterField onto the renamed field (the special-case only applies when
    db_column is None). The operations should remain (i.e. not be turned into
    Rename+Alter on the new name).
    """
    field = models.CharField(max_length=64)
    field.db_column = 'legacy_col'
    ops = [migrations.AlterField('Book', 'title', field), migrations.RenameField('Book', 'title', 'headline')]
    self.assertDoesNotOptimize(ops)

def test_alter_then_remove_field_case_insensitive(self):
    """
    A RemoveField following an AlterField on the same field (case-insensitive)
    should absorb the AlterField and leave only the RemoveField.
    """
    ops = [migrations.AlterField('Foo', 'age', models.IntegerField()), migrations.RemoveField('foo', 'AGE')]
    expected = [migrations.RemoveField('foo', 'AGE')]
    self.assertOptimizesTo(ops, expected)

def test_alter_on_different_fields_does_not_collapse(self):
    """
    AlterField operations on different fields must not be collapsed.
    """
    ops = [migrations.AlterField('Foo', 'a', models.IntegerField()), migrations.AlterField('Foo', 'b', models.IntegerField())]
    self.assertDoesNotOptimize(ops)

def test_alter_preserve_default_flag_respected_when_collapsing(self):
    """
    When collapsing successive AlterField operations, the final operation's
    preserve_default value should be the one that remains.
    """
    ops = [migrations.AlterField('Foo', 'score', models.FloatField(default=1.0), preserve_default=False), migrations.AlterField('Foo', 'score', models.FloatField(default=2.0))]
    expected = [migrations.AlterField('Foo', 'score', models.FloatField(default=2.0))]
    self.assertOptimizesTo(ops, expected)

def test_alter_then_rename_then_alter_results_in_rename_then_alter(self):
    """
    A pattern AlterField -> RenameField -> AlterField (on the new name) should
    be optimized into RenameField followed by a single AlterField on the final name.
    """
    initial = models.CharField(max_length=120)
    after_first_alter = models.CharField(max_length=80)
    ops = [migrations.AlterField('Book', 'title', initial), migrations.RenameField('Book', 'title', 'headline'), migrations.AlterField('Book', 'headline', after_first_alter)]
    expected = [migrations.RenameField('Book', 'title', 'headline'), migrations.AlterField('Book', 'headline', after_first_alter)]
    self.assertOptimizesTo(ops, expected)