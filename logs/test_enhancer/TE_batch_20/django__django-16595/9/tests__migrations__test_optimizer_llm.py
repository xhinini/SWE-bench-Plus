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