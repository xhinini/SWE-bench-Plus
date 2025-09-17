import unittest
from django.db import models
from django.db.models import CharField, Field

class FieldNonDBAttrsTests(unittest.TestCase):

    def test_non_db_attrs_exists_on_field(self):
        self.assertTrue(hasattr(Field, 'non_db_attrs'))

    def test_non_db_attrs_is_tuple(self):
        non_db = getattr(Field, 'non_db_attrs')
        self.assertIsInstance(non_db, tuple)

    def test_non_db_attrs_contains_choices(self):
        non_db = getattr(Field, 'non_db_attrs')
        self.assertIn('choices', non_db)

    def test_non_db_attrs_contains_db_column(self):
        non_db = getattr(Field, 'non_db_attrs')
        self.assertIn('db_column', non_db)

    def test_non_db_attrs_contains_validators(self):
        non_db = getattr(Field, 'non_db_attrs')
        self.assertIn('validators', non_db)

    def test_non_db_attrs_contains_verbose_name(self):
        non_db = getattr(Field, 'non_db_attrs')
        self.assertIn('verbose_name', non_db)

    def test_non_db_attrs_contains_on_delete(self):
        non_db = getattr(Field, 'non_db_attrs')
        self.assertIn('on_delete', non_db)

    def test_non_db_attrs_inherited_by_subclass(self):
        self.assertTrue(hasattr(CharField, 'non_db_attrs'))
        self.assertEqual(getattr(CharField, 'non_db_attrs'), getattr(Field, 'non_db_attrs'))

    def test_non_db_attrs_expected_contents(self):
        non_db = set(getattr(Field, 'non_db_attrs'))
        expected = {'blank', 'choices', 'db_column', 'editable', 'error_messages', 'help_text', 'limit_choices_to', 'on_delete', 'related_name', 'related_query_name', 'validators', 'verbose_name'}
        self.assertTrue(expected.issubset(non_db))

def _make_custom_field_subclass(parent, extra_attr_name):
    """
    Helper to dynamically create a Field subclass that extends parent's
    non_db_attrs with one extra attribute name.
    """
    class_name = 'Custom%s' % parent.__name__
    non_db_attrs = parent.non_db_attrs + (extra_attr_name,)
    attrs = {'non_db_attrs': non_db_attrs}
    return type(class_name, (parent,), attrs)

@isolate_apps('schema')
def test_alter_charfield_with_custom_non_db_attr_noop(self):
    CustomCharField = _make_custom_field_subclass(CharField, 'custom_opt')

    class Foo(Model):
        name = CustomCharField(max_length=50)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('name')
    new_field = copy(old_field)
    new_field.custom_opt = 'value'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_textfield_with_custom_non_db_attr_noop(self):
    CustomTextField = _make_custom_field_subclass(TextField, 'custom_meta')

    class Foo(Model):
        info = CustomTextField()

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('info')
    new_field = copy(old_field)
    new_field.custom_meta = {'x': 1}
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_integerfield_with_custom_non_db_attr_noop(self):
    CustomIntegerField = _make_custom_field_subclass(IntegerField, 'custom_flag')

    class Foo(Model):
        num = CustomIntegerField(null=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('num')
    new_field = copy(old_field)
    new_field.custom_flag = True
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_datefield_with_custom_non_db_attr_noop(self):
    CustomDateField = _make_custom_field_subclass(DateField, 'custom_note')

    class Foo(Model):
        d = CustomDateField(null=True, blank=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('d')
    new_field = copy(old_field)
    new_field.custom_note = 'note'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_datetimefield_with_custom_non_db_attr_noop(self):
    CustomDateTimeField = _make_custom_field_subclass(DateTimeField, 'meta_x')

    class Foo(Model):
        dt = CustomDateTimeField(null=True, blank=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('dt')
    new_field = copy(old_field)
    new_field.meta_x = 123
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_timefield_with_custom_non_db_attr_noop(self):
    CustomTimeField = _make_custom_field_subclass(TimeField, 'display_hint')

    class Foo(Model):
        t = CustomTimeField(null=True, blank=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('t')
    new_field = copy(old_field)
    new_field.display_hint = 'hh:mm'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_booleanfield_with_custom_non_db_attr_noop(self):
    CustomBooleanField = _make_custom_field_subclass(BooleanField, 'presentation')

    class Foo(Model):
        flag = CustomBooleanField(null=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('flag')
    new_field = copy(old_field)
    new_field.presentation = {'widget': 'toggle'}
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_decimalfield_with_custom_non_db_attr_noop(self):
    CustomDecimalField = _make_custom_field_subclass(DecimalField, 'decimal_marker')

    class Foo(Model):
        val = CustomDecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('val')
    new_field = copy(old_field)
    new_field.decimal_marker = 'm'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_binaryfield_with_custom_non_db_attr_noop(self):
    CustomBinaryField = _make_custom_field_subclass(BinaryField, 'bin_meta')

    class Foo(Model):
        bits = CustomBinaryField(blank=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('bits')
    new_field = copy(old_field)
    new_field.bin_meta = b'abc'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_uuidfield_with_custom_non_db_attr_noop(self):
    CustomUUIDField = _make_custom_field_subclass(UUIDField, 'uuid_note')

    class Foo(Model):
        u = CustomUUIDField(null=True, blank=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('u')
    new_field = copy(old_field)
    new_field.uuid_note = 'no-db-impact'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)