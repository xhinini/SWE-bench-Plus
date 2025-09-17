def test_alter_model_options_remove_all_when_empty(self):
    """
    If AlterModelOptions provides an empty options dict, all ALTER_OPTION_KEYS
    present on the CreateModel should be removed; non-ALTER keys should be
    preserved (see other tests).
    """
    self.assertOptimizesTo([migrations.CreateModel('TmpModel', fields=[], options={'ordering': ['id'], 'verbose_name': 'Tmp'}), migrations.AlterModelOptions('TmpModel', options={})], [migrations.CreateModel('TmpModel', fields=[])])

def test_alter_model_options_preserve_non_alter_keys(self):
    """
    Non-ALTER_OPTION_KEYS (e.g., db_table) should be preserved when an
    AlterModelOptions operation removes ALTER keys.
    """
    self.assertOptimizesTo([migrations.CreateModel('TblModel', fields=[], options={'db_table': 'custom_table', 'ordering': ['id']}), migrations.AlterModelOptions('TblModel', options={})], [migrations.CreateModel('TblModel', fields=[], options={'db_table': 'custom_table'})])

def test_alter_model_options_partial_update_removes_unmentioned_alter_keys(self):
    """
    When AlterModelOptions partially updates ALTER_OPTION_KEYS, keys not
    mentioned should be removed from the merged options.
    """
    self.assertOptimizesTo([migrations.CreateModel('PartialModel', fields=[], options={'ordering': ['id'], 'verbose_name': 'OldName', 'permissions': [('can_test', 'Can test')]}), migrations.AlterModelOptions('PartialModel', options={'ordering': ['-id']})], [migrations.CreateModel('PartialModel', fields=[], options={'ordering': ['-id']})])

def test_alter_model_options_handles_boolean_values_and_removes_other_alter_keys(self):
    """
    Boolean ALTER_OPTION_KEYS should be updated when present, and other
    ALTER_OPTION_KEYS not present in the alter should be removed.
    """
    self.assertOptimizesTo([migrations.CreateModel('ManagedModel', fields=[], options={'managed': True, 'ordering': ['id']}), migrations.AlterModelOptions('ManagedModel', options={'managed': False})], [migrations.CreateModel('ManagedModel', fields=[], options={'managed': False})])

def test_alter_model_options_preserve_non_alter_with_falsy_value(self):
    """
    Non-ALTER_OPTION_KEYS that are falsy (e.g., db_table=None) should still be
    preserved when ALTER_OPTION_KEYS are removed.
    """
    self.assertOptimizesTo([migrations.CreateModel('FalsyModel', fields=[], options={'db_table': None, 'ordering': ['id']}), migrations.AlterModelOptions('FalsyModel', options={})], [migrations.CreateModel('FalsyModel', fields=[], options={'db_table': None})])

def test_alter_model_options_remove_default_permissions(self):
    """
    Confirm default_permissions (an ALTER_OPTION_KEY) is removed when not
    provided in the AlterModelOptions.
    """
    self.assertOptimizesTo([migrations.CreateModel('PermModel', fields=[], options={'default_permissions': ('add', 'change'), 'ordering': ['id']}), migrations.AlterModelOptions('PermModel', options={})], [migrations.CreateModel('PermModel', fields=[])])

def test_alter_model_options_add_verbose_name_plural_and_remove_others(self):
    """
    Adding only verbose_name_plural should replace any existing ALTER_OPTION_KEYS
    and remove others not present in the alter.
    """
    self.assertOptimizesTo([migrations.CreateModel('PluralModel', fields=[], options={'ordering': ['id'], 'verbose_name': 'One'}), migrations.AlterModelOptions('PluralModel', options={'verbose_name_plural': 'Ones'})], [migrations.CreateModel('PluralModel', fields=[], options={'verbose_name_plural': 'Ones'})])

def test_alter_model_options_get_latest_by_removed_when_absent(self):
    """
    get_latest_by should be removed when not included in the AlterModelOptions.
    """
    self.assertOptimizesTo([migrations.CreateModel('LatestModel', fields=[], options={'get_latest_by': 'created', 'verbose_name': 'L'}), migrations.AlterModelOptions('LatestModel', options={})], [migrations.CreateModel('LatestModel', fields=[])])

def test_alter_model_options_preserve_key_when_set_to_none(self):
    """
    If an AlterModelOptions explicitly sets an ALTER_OPTION_KEY to None, the
    key should be present with the None value (i.e., presence matters).
    """
    self.assertOptimizesTo([migrations.CreateModel('NoneModel', fields=[], options={'get_latest_by': 'created', 'verbose_name': 'N'}), migrations.AlterModelOptions('NoneModel', options={'get_latest_by': None})], [migrations.CreateModel('NoneModel', fields=[], options={'get_latest_by': None})])

def test_alter_model_options_complex_combination(self):
    """
    Complex case: preserve non-alter keys, update some alter keys, remove others.
    """
    self.assertOptimizesTo([migrations.CreateModel('ComplexModel', fields=[], options={'db_table': 'tbl_complex', 'ordering': ['a'], 'verbose_name': 'ComplexOld'}), migrations.AlterModelOptions('ComplexModel', options={'verbose_name': 'ComplexNew', 'select_on_save': True})], [migrations.CreateModel('ComplexModel', fields=[], options={'db_table': 'tbl_complex', 'verbose_name': 'ComplexNew', 'select_on_save': True})])

def test_create_alter_model_options_removes_ordering_permissions_empty(self):
    """
    If an AlterModelOptions with empty options follows a CreateModel that had
    ALTER_OPTION_KEYS set, those keys should be removed from the resulting
    CreateModel.
    """
    ops = [migrations.CreateModel('MyModel', fields=[], options={'ordering': ['id'], 'permissions': [('can_test', 'Can test')]}), migrations.AlterModelOptions('MyModel', options={})]
    expected = [migrations.CreateModel('MyModel', fields=[])]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_model_options_preserves_non_alter_db_table(self):
    """
    Non-ALTER_OPTION_KEYS (like db_table) should be preserved when altering
    ALTER_OPTION_KEYS.
    """
    ops = [migrations.CreateModel('MyModel', fields=[], options={'db_table': 'custom_table', 'ordering': ['id']}), migrations.AlterModelOptions('MyModel', options={'ordering': ['-id']})]
    expected = [migrations.CreateModel('MyModel', fields=[], options={'db_table': 'custom_table', 'ordering': ['-id']})]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_model_options_removes_unmentioned_alter_keys(self):
    """
    If AlterModelOptions provides only some ALTER_OPTION_KEYS, the other
    ALTER keys previously present on CreateModel should be removed.
    """
    ops = [migrations.CreateModel('MyModel', fields=[], options={'verbose_name': 'My Model', 'ordering': ['id']}), migrations.AlterModelOptions('MyModel', options={'verbose_name': 'A Model'})]
    expected = [migrations.CreateModel('MyModel', fields=[], options={'verbose_name': 'A Model'})]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_model_options_keeps_explicit_false(self):
    """
    If AlterModelOptions explicitly sets a boolean ALTER_OPTION_KEY to False,
    the False value should be preserved (not removed).
    """
    ops = [migrations.CreateModel('MyModel', fields=[], options={'managed': True}), migrations.AlterModelOptions('MyModel', options={'managed': False})]
    expected = [migrations.CreateModel('MyModel', fields=[], options={'managed': False})]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_model_options_keeps_explicit_none(self):
    """
    If AlterModelOptions explicitly sets a key (e.g. get_latest_by) to None,
    the None value should be preserved.
    """
    ops = [migrations.CreateModel('MyModel', fields=[], options={'get_latest_by': 'created'}), migrations.AlterModelOptions('MyModel', options={'get_latest_by': None})]
    expected = [migrations.CreateModel('MyModel', fields=[], options={'get_latest_by': None})]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_model_options_merges_multiple_keys(self):
    """
    AlterModelOptions should merge provided keys and remove unmentioned
    ALTER_OPTION_KEYS from the CreateModel.options.
    """
    ops = [migrations.CreateModel('MyModel', fields=[], options={'ordering': ['id'], 'verbose_name': 'My Model', 'permissions': [('can_test', 'Can test')], 'db_table': 'tbl'}), migrations.AlterModelOptions('MyModel', options={'ordering': ['-id'], 'verbose_name_plural': 'Models'})]
    expected = [migrations.CreateModel('MyModel', fields=[], options={'db_table': 'tbl', 'ordering': ['-id'], 'verbose_name_plural': 'Models'})]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_model_options_empty_removes_all_alter_but_preserves_non_alter(self):
    """
    An empty AlterModelOptions should remove all ALTER_OPTION_KEYS from the
    CreateModel, but should not remove unrelated keys.
    """
    ops = [migrations.CreateModel('MyModel', fields=[], options={'ordering': ['id'], 'verbose_name': 'My Model', 'db_table': 'keep_table'}), migrations.AlterModelOptions('MyModel', options={})]
    expected = [migrations.CreateModel('MyModel', fields=[], options={'db_table': 'keep_table'})]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_model_options_sequential_alter_ops(self):
    """
    A CreateModel followed by two AlterModelOptions should reduce to a single
    CreateModel with the second AlterModelOptions' keys merged and any
    unmentioned ALTER keys removed.
    """
    ops = [migrations.CreateModel('MyModel', fields=[], options={'ordering': ['id'], 'verbose_name': 'My Model', 'permissions': [('can_test', 'Can test')]}), migrations.AlterModelOptions('MyModel', options={'ordering': ['-id']}), migrations.AlterModelOptions('MyModel', options={'verbose_name': 'Renamed'})]
    expected = [migrations.CreateModel('MyModel', fields=[], options={'verbose_name': 'Renamed'})]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_model_options_handles_empty_permissions_set(self):
    """
    If AlterModelOptions explicitly sets 'permissions' to an empty set/list,
    that empty value should be kept (not treated as "not provided").
    """
    ops = [migrations.CreateModel('MyModel', fields=[], options={'permissions': [('can_test', 'Can test')]}), migrations.AlterModelOptions('MyModel', options={'permissions': set()})]
    expected = [migrations.CreateModel('MyModel', fields=[], options={'permissions': set()})]
    self.assertOptimizesTo(ops, expected)

def test_create_alter_model_options_does_not_remove_non_alter_when_alter_is_empty(self):
    """
    Confirm db_table (non-ALTER key) is not removed when AlterModelOptions is empty.
    """
    ops = [migrations.CreateModel('MyModel', fields=[], options={'db_table': 'persist', 'ordering': ['id']}), migrations.AlterModelOptions('MyModel', options={})]
    expected = [migrations.CreateModel('MyModel', fields=[], options={'db_table': 'persist'})]
    self.assertOptimizesTo(ops, expected)