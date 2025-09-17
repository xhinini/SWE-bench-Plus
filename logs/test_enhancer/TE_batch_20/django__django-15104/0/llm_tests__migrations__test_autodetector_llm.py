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