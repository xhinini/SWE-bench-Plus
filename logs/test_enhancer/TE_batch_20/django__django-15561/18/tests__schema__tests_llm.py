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

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_1(self):

    class CustomField1(CharField):
        non_db_attrs = ('custom_1',)

        def __init__(self, *args, custom_1=False, **kwargs):
            kwargs.setdefault('max_length', 10)
            self.custom_1 = custom_1
            super().__init__(*args, **kwargs)

    class M(Model):
        f = CustomField1(custom_1=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = CustomField1(custom_1=False)
    new_field.set_attributes_from_name('f')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_2(self):

    class CustomField2(CharField):
        non_db_attrs = ('opt_flag',)

        def __init__(self, *args, opt_flag=False, **kwargs):
            kwargs.setdefault('max_length', 10)
            self.opt_flag = opt_flag
            super().__init__(*args, **kwargs)

    class M(Model):
        f = CustomField2(opt_flag=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = CustomField2(opt_flag=False)
    new_field.set_attributes_from_name('f')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_3(self):

    class CustomField3(CharField):
        non_db_attrs = ('ui_hint',)

        def __init__(self, *args, ui_hint=None, **kwargs):
            kwargs.setdefault('max_length', 10)
            self.ui_hint = ui_hint
            super().__init__(*args, **kwargs)

    class M(Model):
        f = CustomField3(ui_hint='big')

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = CustomField3(ui_hint='small')
    new_field.set_attributes_from_name('f')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_4(self):

    class CustomField4(CharField):
        non_db_attrs = ('presentation',)

        def __init__(self, *args, presentation=None, **kwargs):
            kwargs.setdefault('max_length', 10)
            self.presentation = presentation
            super().__init__(*args, **kwargs)

    class M(Model):
        f = CustomField4(presentation='alpha')

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = CustomField4(presentation='beta')
    new_field.set_attributes_from_name('f')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_5(self):

    class CustomField5(CharField):
        non_db_attrs = ('display_order',)

        def __init__(self, *args, display_order=0, **kwargs):
            kwargs.setdefault('max_length', 10)
            self.display_order = display_order
            super().__init__(*args, **kwargs)

    class M(Model):
        f = CustomField5(display_order=1)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = CustomField5(display_order=2)
    new_field.set_attributes_from_name('f')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_6(self):

    class CustomField6(CharField):
        non_db_attrs = ('widget_attrs',)

        def __init__(self, *args, widget_attrs=None, **kwargs):
            kwargs.setdefault('max_length', 10)
            self.widget_attrs = widget_attrs
            super().__init__(*args, **kwargs)

    class M(Model):
        f = CustomField6(widget_attrs={'class': 'a'})

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = CustomField6(widget_attrs={'class': 'b'})
    new_field.set_attributes_from_name('f')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_7(self):

    class CustomField7(CharField):
        non_db_attrs = ('ui_group',)

        def __init__(self, *args, ui_group=None, **kwargs):
            kwargs.setdefault('max_length', 10)
            self.ui_group = ui_group
            super().__init__(*args, **kwargs)

    class M(Model):
        f = CustomField7(ui_group='A')

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = CustomField7(ui_group='B')
    new_field.set_attributes_from_name('f')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_8(self):

    class CustomField8(CharField):
        non_db_attrs = ('presentation_hint',)

        def __init__(self, *args, presentation_hint=None, **kwargs):
            kwargs.setdefault('max_length', 10)
            self.presentation_hint = presentation_hint
            super().__init__(*args, **kwargs)

    class M(Model):
        f = CustomField8(presentation_hint='X')

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = CustomField8(presentation_hint='Y')
    new_field.set_attributes_from_name('f')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_9(self):

    class CustomField9(CharField):
        non_db_attrs = ('render_flag',)

        def __init__(self, *args, render_flag=False, **kwargs):
            kwargs.setdefault('max_length', 10)
            self.render_flag = render_flag
            super().__init__(*args, **kwargs)

    class M(Model):
        f = CustomField9(render_flag=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = CustomField9(render_flag=False)
    new_field.set_attributes_from_name('f')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_10(self):

    class CustomField10(CharField):
        non_db_attrs = ('admin_only',)

        def __init__(self, *args, admin_only=False, **kwargs):
            kwargs.setdefault('max_length', 10)
            self.admin_only = admin_only
            super().__init__(*args, **kwargs)

    class M(Model):
        f = CustomField10(admin_only=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = CustomField10(admin_only=False)
    new_field.set_attributes_from_name('f')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_charfield_custom_non_db_attr_noop(self):

    class MyCharField(CharField):
        non_db_attrs = CharField.non_db_attrs + ('_custom_flag',)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            if getattr(self, '_custom_flag', None) is not None:
                kwargs['_custom_flag'] = self._custom_flag
            return (name, path, args, kwargs)

    class M(Model):
        f = MyCharField(max_length=10)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = MyCharField(max_length=10)
    new_field.set_attributes_from_name('f')
    new_field.model = M
    new_field._custom_flag = True
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_integerfield_custom_non_db_attr_noop(self):

    class MyIntegerField(IntegerField):
        non_db_attrs = IntegerField.non_db_attrs + ('_meta_note',)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            if getattr(self, '_meta_note', None) is not None:
                kwargs['_meta_note'] = self._meta_note
            return (name, path, args, kwargs)

    class M(Model):
        f = MyIntegerField(null=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = MyIntegerField(null=True)
    new_field.set_attributes_from_name('f')
    new_field.model = M
    new_field._meta_note = 'note'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_booleanfield_custom_non_db_attr_noop(self):

    class MyBooleanField(BooleanField):
        non_db_attrs = BooleanField.non_db_attrs + ('_ui_hint',)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            if getattr(self, '_ui_hint', None) is not None:
                kwargs['_ui_hint'] = self._ui_hint
            return (name, path, args, kwargs)

    class M(Model):
        f = MyBooleanField(null=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = MyBooleanField(null=True)
    new_field.set_attributes_from_name('f')
    new_field.model = M
    new_field._ui_hint = 'render_as_toggle'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_datetimefield_custom_non_db_attr_noop(self):

    class MyDateTimeField(DateTimeField):
        non_db_attrs = DateTimeField.non_db_attrs + ('_display_tz',)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            if getattr(self, '_display_tz', None) is not None:
                kwargs['_display_tz'] = self._display_tz
            return (name, path, args, kwargs)

    class M(Model):
        f = MyDateTimeField(null=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = MyDateTimeField(null=True)
    new_field.set_attributes_from_name('f')
    new_field.model = M
    new_field._display_tz = 'UTC'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_textfield_custom_non_db_attr_noop(self):

    class MyTextField(TextField):
        non_db_attrs = TextField.non_db_attrs + ('_extra_label',)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            if getattr(self, '_extra_label', None) is not None:
                kwargs['_extra_label'] = self._extra_label
            return (name, path, args, kwargs)

    class M(Model):
        f = MyTextField()

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = MyTextField()
    new_field.set_attributes_from_name('f')
    new_field.model = M
    new_field._extra_label = 'long text'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_binaryfield_custom_non_db_attr_noop(self):

    class MyBinaryField(BinaryField):
        non_db_attrs = BinaryField.non_db_attrs + ('_binary_hint',)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            if getattr(self, '_binary_hint', None) is not None:
                kwargs['_binary_hint'] = self._binary_hint
            return (name, path, args, kwargs)

    class M(Model):
        f = MyBinaryField(blank=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = MyBinaryField(blank=True)
    new_field.set_attributes_from_name('f')
    new_field.model = M
    new_field._binary_hint = 'base64'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_uuidfield_custom_non_db_attr_noop(self):

    class MyUUIDField(UUIDField):
        non_db_attrs = UUIDField.non_db_attrs + ('_ui_format',)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            if getattr(self, '_ui_format', None) is not None:
                kwargs['_ui_format'] = self._ui_format
            return (name, path, args, kwargs)

    class M(Model):
        f = MyUUIDField(null=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = MyUUIDField(null=True)
    new_field.set_attributes_from_name('f')
    new_field.model = M
    new_field._ui_format = 'hyphenated'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_decimalfield_custom_non_db_attr_noop(self):

    class MyDecimalField(DecimalField):
        non_db_attrs = DecimalField.non_db_attrs + ('_display_precision',)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            if getattr(self, '_display_precision', None) is not None:
                kwargs['_display_precision'] = self._display_precision
            return (name, path, args, kwargs)

    class M(Model):
        f = MyDecimalField(max_digits=5, decimal_places=2, null=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = MyDecimalField(max_digits=5, decimal_places=2, null=True)
    new_field.set_attributes_from_name('f')
    new_field.model = M
    new_field._display_precision = 3
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_durationfield_custom_non_db_attr_noop(self):

    class MyDurationField(DurationField):
        non_db_attrs = DurationField.non_db_attrs + ('_form_hint',)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            if getattr(self, '_form_hint', None) is not None:
                kwargs['_form_hint'] = self._form_hint
            return (name, path, args, kwargs)

    class M(Model):
        f = MyDurationField(null=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = MyDurationField(null=True)
    new_field.set_attributes_from_name('f')
    new_field.model = M
    new_field._form_hint = 'hh:mm'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_genericipaddressfield_custom_non_db_attr_noop(self):

    class MyIPField(GenericIPAddressField):
        non_db_attrs = GenericIPAddressField.non_db_attrs + ('_ui_version_hint',)

        def deconstruct(self):
            name, path, args, kwargs = super().deconstruct()
            if getattr(self, '_ui_version_hint', None) is not None:
                kwargs['_ui_version_hint'] = self._ui_version_hint
            return (name, path, args, kwargs)

    class M(Model):
        f = MyIPField(protocol='both', unpack_ipv4=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(M)
    old_field = M._meta.get_field('f')
    new_field = MyIPField(protocol='both', unpack_ipv4=True)
    new_field.set_attributes_from_name('f')
    new_field.model = M
    new_field._ui_version_hint = 'v6_preferred'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(M, old_field, new_field, strict=True)

def test_alter_field_help_text_noop_extra(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, CASCADE, help_text='a new help text')
    new_field.set_attributes_from_name('author')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

def test_alter_field_verbose_name_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, CASCADE, verbose_name='a verbose name')
    new_field.set_attributes_from_name('author')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

def test_alter_field_validators_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, CASCADE, validators=[lambda x: x], related_name='irrelevant')
    new_field.set_attributes_from_name('author')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

def test_alter_field_error_messages_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, CASCADE, error_messages={'invalid': 'custom'}, related_query_name='q')
    new_field.set_attributes_from_name('author')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

def test_alter_field_editable_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, CASCADE, editable=False)
    new_field.set_attributes_from_name('author')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

def test_alter_field_related_name_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, CASCADE, related_name='new_rel_name')
    new_field.set_attributes_from_name('author')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

def test_alter_field_limit_choices_to_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, CASCADE, limit_choices_to={'a': 'b'})
    new_field.set_attributes_from_name('author')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

def test_alter_field_blank_only_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, CASCADE, blank=True)
    new_field.set_attributes_from_name('author')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

def test_alter_charfield_choices_noop_extra(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    old_field = Author._meta.get_field('name')
    new_field = CharField(max_length=255, choices=(('A', 'A'), ('B', 'B')))
    new_field.set_attributes_from_name('name')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, old_field, new_field, strict=True)

def test_alter_field_add_non_db_attr_on_new_field_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, CASCADE)
    new_field.set_attributes_from_name('author')
    new_field.help_text = 'only-on-new'
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_charfield_no_queries(self):

    class CustomCharField(CharField):
        non_db_attrs = CharField.non_db_attrs + ('my_custom',)

        def __init__(self, *args, my_custom=False, **kwargs):
            self.my_custom = my_custom
            super().__init__(*args, **kwargs)

    class Foo(Model):
        name = CustomCharField(max_length=20)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('name')
    new_field = copy(old_field)
    new_field.my_custom = True
    new_field.set_attributes_from_name('name')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_integerfield_no_queries(self):

    class CustomIntegerField(IntegerField):
        non_db_attrs = IntegerField.non_db_attrs + ('my_custom',)

        def __init__(self, *args, my_custom=False, **kwargs):
            self.my_custom = my_custom
            super().__init__(*args, **kwargs)

    class Foo(Model):
        num = CustomIntegerField()

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('num')
    new_field = copy(old_field)
    new_field.my_custom = True
    new_field.set_attributes_from_name('num')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_textfield_no_queries(self):

    class CustomTextField(TextField):
        non_db_attrs = TextField.non_db_attrs + ('my_custom',)

        def __init__(self, *args, my_custom=False, **kwargs):
            self.my_custom = my_custom
            super().__init__(*args, **kwargs)

    class Foo(Model):
        info = CustomTextField()

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('info')
    new_field = copy(old_field)
    new_field.my_custom = True
    new_field.set_attributes_from_name('info')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_datefield_no_queries(self):

    class CustomDateField(DateField):
        non_db_attrs = DateField.non_db_attrs + ('my_custom',)

        def __init__(self, *args, my_custom=False, **kwargs):
            self.my_custom = my_custom
            super().__init__(*args, **kwargs)

    class Foo(Model):
        d = CustomDateField()

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('d')
    new_field = copy(old_field)
    new_field.my_custom = True
    new_field.set_attributes_from_name('d')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_datetimefield_no_queries(self):

    class CustomDateTimeField(DateTimeField):
        non_db_attrs = DateTimeField.non_db_attrs + ('my_custom',)

        def __init__(self, *args, my_custom=False, **kwargs):
            self.my_custom = my_custom
            super().__init__(*args, **kwargs)

    class Foo(Model):
        dt = CustomDateTimeField()

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('dt')
    new_field = copy(old_field)
    new_field.my_custom = True
    new_field.set_attributes_from_name('dt')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_timefield_no_queries(self):

    class CustomTimeField(TimeField):
        non_db_attrs = TimeField.non_db_attrs + ('my_custom',)

        def __init__(self, *args, my_custom=False, **kwargs):
            self.my_custom = my_custom
            super().__init__(*args, **kwargs)

    class Foo(Model):
        t = CustomTimeField()

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('t')
    new_field = copy(old_field)
    new_field.my_custom = True
    new_field.set_attributes_from_name('t')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_decimalfield_no_queries(self):

    class CustomDecimalField(DecimalField):
        non_db_attrs = DecimalField.non_db_attrs + ('my_custom',)

        def __init__(self, *args, my_custom=False, **kwargs):
            self.my_custom = my_custom
            super().__init__(*args, **kwargs)

    class Foo(Model):
        val = CustomDecimalField(max_digits=5, decimal_places=2)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('val')
    new_field = copy(old_field)
    new_field.my_custom = True
    new_field.set_attributes_from_name('val')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_uuidfield_no_queries(self):

    class CustomUUIDField(UUIDField):
        non_db_attrs = UUIDField.non_db_attrs + ('my_custom',)

        def __init__(self, *args, my_custom=False, **kwargs):
            self.my_custom = my_custom
            super().__init__(*args, **kwargs)

    class Foo(Model):
        u = CustomUUIDField()

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('u')
    new_field = copy(old_field)
    new_field.my_custom = True
    new_field.set_attributes_from_name('u')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_binaryfield_no_queries(self):

    class CustomBinaryField(BinaryField):
        non_db_attrs = BinaryField.non_db_attrs + ('my_custom',)

        def __init__(self, *args, my_custom=False, **kwargs):
            self.my_custom = my_custom
            super().__init__(*args, **kwargs)

    class Foo(Model):
        data = CustomBinaryField(blank=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('data')
    new_field = copy(old_field)
    new_field.my_custom = True
    new_field.set_attributes_from_name('data')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_noop_a(self):

    class MyCharFieldA(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_a',)

        def __init__(self, *args, custom_a=False, **kwargs):
            self.custom_a = custom_a
            super().__init__(*args, **kwargs)

    class FooA(Model):
        name = MyCharFieldA(max_length=255, custom_a=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(FooA)
    old_field = FooA._meta.get_field('name')
    new_field = CharField(max_length=255)
    new_field.set_attributes_from_name('name')
    new_field.model = FooA
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooA, old_field, new_field, strict=True)
    new_field2 = MyCharFieldA(max_length=255, custom_a=True)
    new_field2.set_attributes_from_name('name')
    new_field2.model = FooA
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooA, new_field, new_field2, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_noop_b(self):

    class MyCharFieldB(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_b',)

        def __init__(self, *args, custom_b=None, **kwargs):
            self.custom_b = custom_b
            super().__init__(*args, **kwargs)

    class FooB(Model):
        name = MyCharFieldB(max_length=255, custom_b='x')

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(FooB)
    old_field = FooB._meta.get_field('name')
    new_field = CharField(max_length=255)
    new_field.set_attributes_from_name('name')
    new_field.model = FooB
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooB, old_field, new_field, strict=True)
    new_field2 = MyCharFieldB(max_length=255, custom_b='x')
    new_field2.set_attributes_from_name('name')
    new_field2.model = FooB
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooB, new_field, new_field2, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_noop_c(self):

    class MyCharFieldC(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_c',)

        def __init__(self, *args, custom_c=0, **kwargs):
            self.custom_c = custom_c
            super().__init__(*args, **kwargs)

    class FooC(Model):
        name = MyCharFieldC(max_length=255, custom_c=1)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(FooC)
    old_field = FooC._meta.get_field('name')
    new_field = CharField(max_length=255)
    new_field.set_attributes_from_name('name')
    new_field.model = FooC
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooC, old_field, new_field, strict=True)
    new_field2 = MyCharFieldC(max_length=255, custom_c=1)
    new_field2.set_attributes_from_name('name')
    new_field2.model = FooC
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooC, new_field, new_field2, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_noop_d(self):

    class MyCharFieldD(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_d',)

        def __init__(self, *args, custom_d=None, **kwargs):
            self.custom_d = custom_d
            super().__init__(*args, **kwargs)

    class FooD(Model):
        name = MyCharFieldD(max_length=255, custom_d={'a': 1})

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(FooD)
    old_field = FooD._meta.get_field('name')
    new_field = CharField(max_length=255)
    new_field.set_attributes_from_name('name')
    new_field.model = FooD
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooD, old_field, new_field, strict=True)
    new_field2 = MyCharFieldD(max_length=255, custom_d={'a': 1})
    new_field2.set_attributes_from_name('name')
    new_field2.model = FooD
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooD, new_field, new_field2, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_noop_e(self):

    class MyCharFieldE(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_e',)

        def __init__(self, *args, custom_e=False, **kwargs):
            self.custom_e = custom_e
            super().__init__(*args, **kwargs)

    class FooE(Model):
        name = MyCharFieldE(max_length=255, custom_e=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(FooE)
    old_field = FooE._meta.get_field('name')
    new_field = CharField(max_length=255)
    new_field.set_attributes_from_name('name')
    new_field.model = FooE
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooE, old_field, new_field, strict=True)
    new_field2 = MyCharFieldE(max_length=255, custom_e=True)
    new_field2.set_attributes_from_name('name')
    new_field2.model = FooE
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooE, new_field, new_field2, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_noop_f(self):

    class MyCharFieldF(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_f',)

        def __init__(self, *args, custom_f=(), **kwargs):
            self.custom_f = custom_f
            super().__init__(*args, **kwargs)

    class FooF(Model):
        name = MyCharFieldF(max_length=255, custom_f=(1, 2, 3))

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(FooF)
    old_field = FooF._meta.get_field('name')
    new_field = CharField(max_length=255)
    new_field.set_attributes_from_name('name')
    new_field.model = FooF
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooF, old_field, new_field, strict=True)
    new_field2 = MyCharFieldF(max_length=255, custom_f=(1, 2, 3))
    new_field2.set_attributes_from_name('name')
    new_field2.model = FooF
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooF, new_field, new_field2, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_noop_g(self):

    class MyCharFieldG(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_g',)

        def __init__(self, *args, custom_g=None, **kwargs):
            self.custom_g = custom_g
            super().__init__(*args, **kwargs)

    class FooG(Model):
        name = MyCharFieldG(max_length=255, custom_g=42)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(FooG)
    old_field = FooG._meta.get_field('name')
    new_field = CharField(max_length=255)
    new_field.set_attributes_from_name('name')
    new_field.model = FooG
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooG, old_field, new_field, strict=True)
    new_field2 = MyCharFieldG(max_length=255, custom_g=42)
    new_field2.set_attributes_from_name('name')
    new_field2.model = FooG
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooG, new_field, new_field2, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_noop_h(self):

    class MyCharFieldH(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_h',)

        def __init__(self, *args, custom_h='h', **kwargs):
            self.custom_h = custom_h
            super().__init__(*args, **kwargs)

    class FooH(Model):
        name = MyCharFieldH(max_length=255, custom_h='h')

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(FooH)
    old_field = FooH._meta.get_field('name')
    new_field = CharField(max_length=255)
    new_field.set_attributes_from_name('name')
    new_field.model = FooH
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooH, old_field, new_field, strict=True)
    new_field2 = MyCharFieldH(max_length=255, custom_h='h')
    new_field2.set_attributes_from_name('name')
    new_field2.model = FooH
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooH, new_field, new_field2, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_noop_i(self):

    class MyCharFieldI(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_i',)

        def __init__(self, *args, custom_i=None, **kwargs):
            self.custom_i = custom_i
            super().__init__(*args, **kwargs)

    class FooI(Model):
        name = MyCharFieldI(max_length=255, custom_i=object())

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(FooI)
    old_field = FooI._meta.get_field('name')
    new_field = CharField(max_length=255)
    new_field.set_attributes_from_name('name')
    new_field.model = FooI
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooI, old_field, new_field, strict=True)
    new_field2 = MyCharFieldI(max_length=255, custom_i=old_field.custom_i)
    new_field2.set_attributes_from_name('name')
    new_field2.model = FooI
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooI, new_field, new_field2, strict=True)

@isolate_apps('schema')
def test_custom_non_db_attr_noop_j(self):

    class MyCharFieldJ(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_j',)

        def __init__(self, *args, custom_j=None, **kwargs):
            self.custom_j = custom_j
            super().__init__(*args, **kwargs)

    class FooJ(Model):
        name = MyCharFieldJ(max_length=255, custom_j=({'x': 1},))

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(FooJ)
    old_field = FooJ._meta.get_field('name')
    new_field = CharField(max_length=255)
    new_field.set_attributes_from_name('name')
    new_field.model = FooJ
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooJ, old_field, new_field, strict=True)
    new_field2 = MyCharFieldJ(max_length=255, custom_j=old_field.custom_j)
    new_field2.set_attributes_from_name('name')
    new_field2.model = FooJ
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(FooJ, new_field, new_field2, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_same_class(self):

    class CustomCharField(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_opt',)

    class Foo(Model):
        name = CustomCharField(max_length=10, custom_opt=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('name')
    new_field = CustomCharField(max_length=10, custom_opt=False)
    new_field.set_attributes_from_name('name')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_old_custom_new_plain(self):

    class CustomCharField(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_opt',)

    class Foo(Model):
        name = CustomCharField(max_length=10, custom_opt=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('name')
    new_field = CharField(max_length=10)
    new_field.set_attributes_from_name('name')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_noop_plain_new_custom(self):

    class CustomCharField(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_opt',)

    class Foo(Model):
        name = CharField(max_length=10)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('name')
    new_field = CustomCharField(max_length=10, custom_opt=True)
    new_field.set_attributes_from_name('name')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_two_custom_attrs_noop_different_classes(self):

    class FieldA(CharField):
        non_db_attrs = CharField.non_db_attrs + ('opt_a',)

    class FieldB(CharField):
        non_db_attrs = CharField.non_db_attrs + ('opt_b',)

    class Foo(Model):
        name = FieldA(max_length=10, opt_a=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('name')
    new_field = FieldB(max_length=10, opt_b=True)
    new_field.set_attributes_from_name('name')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_multiple_attrs_noop(self):

    class MultiOptField(CharField):
        non_db_attrs = CharField.non_db_attrs + ('opt1', 'opt2')

    class Foo(Model):
        name = MultiOptField(max_length=10, opt1=1, opt2=2)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('name')
    new_field = MultiOptField(max_length=10, opt1=3, opt2=4)
    new_field.set_attributes_from_name('name')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_copy_and_modify(self):

    class CustomCharField(CharField):
        non_db_attrs = CharField.non_db_attrs + ('custom_opt',)

    class Foo(Model):
        name = CustomCharField(max_length=10, custom_opt=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('name')
    new_field = CustomCharField(max_length=10, custom_opt=False)
    new_field.set_attributes_from_name('name')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_old_and_new_share_name(self):

    class Custom1(CharField):
        non_db_attrs = CharField.non_db_attrs + ('flag',)

    class Custom2(CharField):
        non_db_attrs = CharField.non_db_attrs + ('flag',)

    class Foo(Model):
        name = Custom1(max_length=10, flag=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('name')
    new_field = Custom2(max_length=10, flag=False)
    new_field.set_attributes_from_name('name')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_new_has_extra_non_db(self):

    class BaseField(CharField):
        pass

    class NewField(CharField):
        non_db_attrs = CharField.non_db_attrs + ('extra',)

    class Foo(Model):
        name = BaseField(max_length=10)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('name')
    new_field = NewField(max_length=10, extra=True)
    new_field.set_attributes_from_name('name')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

@isolate_apps('schema')
def test_alter_field_custom_non_db_attr_old_has_extra_non_db(self):

    class OldField(CharField):
        non_db_attrs = CharField.non_db_attrs + ('legacy',)

    class BaseField(CharField):
        pass

    class Foo(Model):
        name = OldField(max_length=10, legacy=True)

        class Meta:
            app_label = 'schema'
    with connection.schema_editor() as editor:
        editor.create_model(Foo)
    old_field = Foo._meta.get_field('name')
    new_field = BaseField(max_length=10)
    new_field.set_attributes_from_name('name')
    new_field.model = Foo
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Foo, old_field, new_field, strict=True)

def test_alter_field_verbose_name_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    old_field = Author._meta.get_field('name')
    new_field = copy(old_field)
    new_field.verbose_name = 'a different verbose name'
    new_field.set_attributes_from_name('name')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, old_field, new_field, strict=True)

def test_alter_field_help_text_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    old_field = Author._meta.get_field('name')
    new_field = copy(old_field)
    new_field.help_text = 'some helpful text'
    new_field.set_attributes_from_name('name')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, old_field, new_field, strict=True)

def test_alter_field_validators_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    old_field = Author._meta.get_field('name')
    new_field = copy(old_field)
    new_field._validators = [lambda x: x]
    new_field.set_attributes_from_name('name')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, old_field, new_field, strict=True)

def test_alter_field_error_messages_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    old_field = Author._meta.get_field('name')
    new_field = copy(old_field)
    new_field._error_messages = {'invalid': 'invalid name'}
    new_field.set_attributes_from_name('name')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, old_field, new_field, strict=True)

def test_alter_field_limit_choices_to_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Book)
        editor.create_model(Author)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, CASCADE, limit_choices_to={'a': 'b'})
    new_field.set_attributes_from_name('author')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

def test_alter_field_blank_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    old_field = Author._meta.get_field('name')
    new_field = copy(old_field)
    new_field.blank = not old_field.blank
    new_field.set_attributes_from_name('name')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, old_field, new_field, strict=True)

def test_alter_field_choices_iterator_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    old_field = Author._meta.get_field('name')
    choices_iter = (c for c in (('Jane', 'Jane'), ('Joe', 'Joe')))
    new_field = CharField(choices=choices_iter, max_length=255)
    new_field.set_attributes_from_name('name')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, old_field, new_field, strict=True)

def test_alter_fk_related_name_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, CASCADE, related_name='new_related_name')
    new_field.set_attributes_from_name('author')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

def test_alter_fk_related_query_name_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, CASCADE, related_query_name='rqn')
    new_field.set_attributes_from_name('author')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

def test_alter_fk_on_delete_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
        editor.create_model(Book)
    old_field = Book._meta.get_field('author')
    new_field = ForeignKey(Author, PROTECT)
    new_field.set_attributes_from_name('author')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)

def test_alter_charfield_choices_noop_variant(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    old_field = Author._meta.get_field('name')
    new_field = CharField(max_length=255, choices=(('Jane', 'Jane'), ('Joe', 'Joe')))
    new_field.set_attributes_from_name('name')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, old_field, new_field, strict=True)
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, new_field, old_field, strict=True)

def test_alter_charfield_choices_noop_on_indexed_field(self):
    with connection.schema_editor() as editor:
        editor.create_model(Book)
    old_field = Book._meta.get_field('title')
    new_field = CharField(max_length=100, db_index=True, choices=(('A', 'A'), ('B', 'B')))
    new_field.set_attributes_from_name('title')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, new_field, old_field, strict=True)

def test_alter_slugfield_choices_noop(self):
    with connection.schema_editor() as editor:
        editor.create_model(Tag)
    old_field = Tag._meta.get_field('slug')
    new_field = SlugField(max_length=50, unique=old_field.unique, choices=(('x', 'x'), ('y', 'y')))
    new_field.set_attributes_from_name('slug')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Tag, old_field, new_field, strict=True)
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Tag, new_field, old_field, strict=True)

def test_alter_field_choices_noop_with_unique(self):
    with connection.schema_editor() as editor:
        editor.create_model(AuthorWithUniqueName)
    old_field = AuthorWithUniqueName._meta.get_field('name')
    new_field = CharField(max_length=255, unique=True, choices=(('u1', 'u1'), ('u2', 'u2')))
    new_field.set_attributes_from_name('name')
    new_field.model = AuthorWithUniqueName
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(AuthorWithUniqueName, old_field, new_field, strict=True)
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(AuthorWithUniqueName, new_field, old_field, strict=True)

def test_alter_field_choices_noop_on_index_from_meta_indexes(self):
    with connection.schema_editor() as editor:
        editor.create_model(AuthorWithIndexedName)
    old_field = AuthorWithIndexedName._meta.get_field('name')
    new_field = CharField(max_length=255, choices=(('i1', 'i1'), ('i2', 'i2')))
    new_field.set_attributes_from_name('name')
    new_field.model = AuthorWithIndexedName
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(AuthorWithIndexedName, old_field, new_field, strict=True)
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(AuthorWithIndexedName, new_field, old_field, strict=True)

def test_alter_field_choices_noop_repeated(self):
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    old_field = Author._meta.get_field('name')
    new_field1 = CharField(max_length=255, choices=(('a', 'a'),))
    new_field1.set_attributes_from_name('name')
    new_field2 = CharField(max_length=255, choices=(('b', 'b'),))
    new_field2.set_attributes_from_name('name')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, old_field, new_field1, strict=True)
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, new_field1, new_field2, strict=True)
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, new_field2, old_field, strict=True)

def test_alter_field_choices_noop_with_generator_choices(self):
    choices_gen = (c for c in [('g1', 'G1'), ('g2', 'G2')])
    with connection.schema_editor() as editor:
        editor.create_model(Author)
    old_field = Author._meta.get_field('name')
    new_field = CharField(max_length=255, choices=choices_gen)
    new_field.set_attributes_from_name('name')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, old_field, new_field, strict=True)
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Author, new_field, old_field, strict=True)

def test_alter_field_choices_noop_preserves_indexes(self):
    with connection.schema_editor() as editor:
        editor.create_model(Book)
    old_field = Book._meta.get_field('title')
    original_indexes = self.get_indexes(Book._meta.db_table)
    new_field = CharField(max_length=100, db_index=True, choices=(('X', 'X'),))
    new_field.set_attributes_from_name('title')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, old_field, new_field, strict=True)
    self.assertEqual(original_indexes, self.get_indexes(Book._meta.db_table))
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Book, new_field, old_field, strict=True)
    self.assertEqual(original_indexes, self.get_indexes(Book._meta.db_table))

def test_alter_text_field_choices_noop_when_supported(self):
    with connection.schema_editor() as editor:
        editor.create_model(Note)
    old_field = Note._meta.get_field('info')
    new_field = TextField(choices=(('t1', 't1'), ('t2', 't2')))
    new_field.set_attributes_from_name('info')
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Note, old_field, new_field, strict=True)
    with connection.schema_editor() as editor, self.assertNumQueries(0):
        editor.alter_field(Note, new_field, old_field, strict=True)