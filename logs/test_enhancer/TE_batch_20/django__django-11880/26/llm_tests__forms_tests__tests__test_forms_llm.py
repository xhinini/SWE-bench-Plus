# No additional imports required (copy is already imported in the test module).
from django.test import SimpleTestCase
from django.forms import CharField, MultiValueField, Form
import copy

class DeepCopyErrorMessagesTests(SimpleTestCase):
    def test_field_deepcopy_shallow_error_messages_shared_value(self):
        class CustomObject:
            def __init__(self, value):
                self.value = value

        class CustomCharField(CharField):
            def __init__(self, **kwargs):
                kwargs.setdefault('error_messages', {})
                kwargs['error_messages']['custom'] = CustomObject('original')
                super().__init__(**kwargs)

        field = CustomCharField()
        field_copy = copy.deepcopy(field)

        # The dict should be a distinct object
        self.assertIsNot(field_copy.error_messages, field.error_messages)
        # But the nested value should be the same object (shallow copy semantics)
        self.assertIs(field_copy.error_messages['custom'], field.error_messages['custom'])

    def test_field_deepcopy_mutating_nested_value_reflects_in_copy(self):
        class CustomObject:
            def __init__(self, value):
                self.value = value

        class CustomCharField(CharField):
            def __init__(self, **kwargs):
                kwargs.setdefault('error_messages', {})
                kwargs['error_messages']['custom'] = CustomObject('original')
                super().__init__(**kwargs)

        field = CustomCharField()
        field_copy = copy.deepcopy(field)

        # Mutate nested object via original
        field.error_messages['custom'].value = 'modified'
        # Mutation should be visible via the copy as well (shared nested object)
        self.assertEqual(field_copy.error_messages['custom'].value, 'modified')

    def test_form_deepcopy_shallow_error_messages_shared_value(self):
        class CustomObject:
            def __init__(self, value):
                self.value = value

        class ProfileForm(Form):
            name = CharField(error_messages={'custom': CustomObject('original')})

        f1 = ProfileForm()
        f2 = copy.deepcopy(f1)

        self.assertIsNot(f2.fields['name'].error_messages, f1.fields['name'].error_messages)
        self.assertIs(
            f2.fields['name'].error_messages['custom'],
            f1.fields['name'].error_messages['custom']
        )

    def test_form_deepcopy_mutating_nested_value_reflects_in_copy(self):
        class CustomObject:
            def __init__(self, value):
                self.value = value

        class ProfileForm(Form):
            name = CharField(error_messages={'custom': CustomObject('original')})

        f1 = ProfileForm()
        f2 = copy.deepcopy(f1)

        # Mutate nested object via original form's field
        f1.fields['name'].error_messages['custom'].value = 'changed'
        # Mutation should be visible via the copy
        self.assertEqual(f2.fields['name'].error_messages['custom'].value, 'changed')

    def test_multivaluefield_subfields_preserve_nested_error_message_identity(self):
        class CustomObject:
            def __init__(self, value):
                self.value = value

        class PhoneField(MultiValueField):
            def __init__(self, *args, **kwargs):
                # Two subfields with custom nested objects in their error_messages
                from django.forms import CharField
                f1 = CharField(error_messages={'incomplete': CustomObject('one')})
                f2 = CharField(error_messages={'incomplete': CustomObject('two')})
                super().__init__(fields=(f1, f2), *args, **kwargs)

            def compress(self, data_list):
                return ' '.join(data_list)

        field = PhoneField()
        field_copy = copy.deepcopy(field)

        # The subfields themselves should be deep-copied (different objects)
        self.assertIsNot(field_copy.fields[0], field.fields[0])
        self.assertIsNot(field_copy.fields[1], field.fields[1])

        # But their error_messages dicts should be distinct objects
        self.assertIsNot(field_copy.fields[0].error_messages, field.fields[0].error_messages)
        # And the nested objects inside those dicts should be the same (shared)
        self.assertIs(field_copy.fields[0].error_messages['incomplete'],
                      field.fields[0].error_messages['incomplete'])
        self.assertIs(field_copy.fields[1].error_messages['incomplete'],
                      field.fields[1].error_messages['incomplete'])

    def test_multivaluefield_in_form_deepcopy_shallow_nested_values(self):
        class CustomObject:
            def __init__(self, value):
                self.value = value

        class PhoneField(MultiValueField):
            def __init__(self, *args, **kwargs):
                from django.forms import CharField
                f1 = CharField(error_messages={'incomplete': CustomObject('one')})
                f2 = CharField(error_messages={'incomplete': CustomObject('two')})
                super().__init__(fields=(f1, f2), *args, **kwargs)

            def compress(self, data_list):
                return ' '.join(data_list)

        class ContainerForm(Form):
            phone = PhoneField()

        f1 = ContainerForm()
        f2 = copy.deepcopy(f1)

        # Distinct dict objects for error_messages
        self.assertIsNot(f1.fields['phone'].fields[0].error_messages,
                         f2.fields['phone'].fields[0].error_messages)
        # But nested objects are shared
        self.assertIs(f1.fields['phone'].fields[0].error_messages['incomplete'],
                      f2.fields['phone'].fields[0].error_messages['incomplete'])

    def test_deepcopy_preserves_shared_mutable_between_multiple_fields(self):
        class CustomObject:
            def __init__(self, value):
                self.value = value

        shared = CustomObject('shared')

        class FormWithTwoFields(Form):
            a = CharField(error_messages={'x': shared})
            b = CharField(error_messages={'x': shared})

        f1 = FormWithTwoFields()
        f2 = copy.deepcopy(f1)

        # The two fields on the original form share the same nested object
        self.assertIs(f1.fields['a'].error_messages['x'], f1.fields['b'].error_messages['x'])
        # The copied form's fields also share the same nested object
        self.assertIs(f2.fields['a'].error_messages['x'], f2.fields['b'].error_messages['x'])
        # And importantly, the nested object should be the same across original and copy
        self.assertIs(f1.fields['a'].error_messages['x'], f2.fields['a'].error_messages['x'])

    def test_deepcopy_error_messages_dicts_are_distinct_but_values_shared(self):
        class CustomObject:
            def __init__(self, value):
                self.value = value

        class CustomCharField(CharField):
            def __init__(self, **kwargs):
                kwargs.setdefault('error_messages', {})
                kwargs['error_messages']['m'] = CustomObject('m')
                super().__init__(**kwargs)

        field = CustomCharField()
        field2 = copy.deepcopy(field)

        # distinct dict containers
        self.assertIsNot(field.error_messages, field2.error_messages)
        # same nested object
        self.assertIs(field.error_messages['m'], field2.error_messages['m'])

    def test_mutation_on_shared_nested_object_reflects_across_many_copies(self):
        class CustomObject:
            def __init__(self, value):
                self.value = value

        class CustomCharField(CharField):
            def __init__(self, **kwargs):
                kwargs.setdefault('error_messages', {})
                kwargs['error_messages']['m'] = CustomObject('orig')
                super().__init__(**kwargs)

        original = CustomCharField()
        c1 = copy.deepcopy(original)
        c2 = copy.deepcopy(original)

        # Mutate nested object via original
        original.error_messages['m'].value = 'changed'
        # Both copies should see the change because the nested object is shared
        self.assertEqual(c1.error_messages['m'].value, 'changed')
        self.assertEqual(c2.error_messages['m'].value, 'changed')

def _make_custom():

    class CustomObject:

        def __init__(self, value):
            self.value = value

        def __repr__(self):
            return '<CustomObject %r>' % (self.value,)
    return CustomObject

def test_field_deepcopy_error_messages_custom_object_identity(self):

    class CustomObj:

        def __init__(self, value):
            self.value = value
    obj = CustomObj('original')
    field = CharField(error_messages={'custom': obj})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom'], obj)
    self.assertIs(field_copy.error_messages['custom'], field.error_messages['custom'])

def test_field_deepcopy_error_messages_custom_object_mutation_reflects(self):

    class CustomObj:

        def __init__(self, value):
            self.value = value
    obj = CustomObj('original')
    field = CharField(error_messages={'custom': obj})
    field_copy = copy.deepcopy(field)
    obj.value = 'changed'
    self.assertEqual(field.error_messages['custom'].value, 'changed')
    self.assertEqual(field_copy.error_messages['custom'].value, 'changed')

def test_field_deepcopy_error_messages_list_identity(self):
    lst = ['a']
    field = CharField(error_messages={'custom': lst})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom'], lst)
    self.assertIs(field_copy.error_messages['custom'], field.error_messages['custom'])

def test_field_deepcopy_error_messages_list_mutation_reflects(self):
    lst = ['a']
    field = CharField(error_messages={'custom': lst})
    field_copy = copy.deepcopy(field)
    lst.append('b')
    self.assertEqual(field.error_messages['custom'], ['a', 'b'])
    self.assertEqual(field_copy.error_messages['custom'], ['a', 'b'])

def test_field_deepcopy_error_messages_dict_identity(self):
    d = {'k': 'v'}
    field = CharField(error_messages={'custom': d})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom'], d)
    self.assertIs(field_copy.error_messages['custom'], field.error_messages['custom'])

def test_field_deepcopy_error_messages_dict_mutation_reflects(self):
    d = {'k': 'v'}
    field = CharField(error_messages={'custom': d})
    field_copy = copy.deepcopy(field)
    d['k2'] = 'v2'
    self.assertIn('k2', field.error_messages['custom'])
    self.assertIn('k2', field_copy.error_messages['custom'])

def test_field_deepcopy_error_messages_nested_mutable_identity(self):
    nested = {'lst': [1, 2]}
    field = CharField(error_messages={'custom': nested})
    field_copy = copy.deepcopy(field)
    self.assertIs(field_copy.error_messages['custom']['lst'], nested['lst'])
    nested['lst'].append(3)
    self.assertEqual(field_copy.error_messages['custom']['lst'], [1, 2, 3])

def test_field_deepcopy_error_messages_bytearray_identity(self):
    b = bytearray(b'abc')
    field = CharField(error_messages={'custom': b})
    field_copy = copy.deepcopy(field)
    self.assertIs(field_copy.error_messages['custom'], b)
    b.extend(b'd')
    self.assertEqual(field_copy.error_messages['custom'], bytearray(b'abcd'))

def test_field_deepcopy_error_messages_set_identity(self):
    s = {'x'}
    field = CharField(error_messages={'custom': s})
    field_copy = copy.deepcopy(field)
    self.assertIs(field_copy.error_messages['custom'], s)
    s.add('y')
    self.assertIn('y', field_copy.error_messages['custom'])

def test_field_deepcopy_error_messages_multiple_values_identity(self):
    obj = {'a': []}
    lst = [obj, obj]
    field = CharField(error_messages={'custom1': obj, 'custom2': lst})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom1'], obj)
    self.assertIs(field_copy.error_messages['custom2'][0], obj)

def test_field_deepcopy_error_messages_value_identity_field(self):

    class CustomMessage:

        def __init__(self, text):
            self.text = text
    f = forms.Field(error_messages={'custom': CustomMessage('original')})
    f2 = copy.deepcopy(f)
    self.assertIsNot(f2.error_messages, f.error_messages)
    self.assertIs(f2.error_messages['custom'], f.error_messages['custom'])
    f.error_messages['custom'].text = 'changed'
    self.assertEqual(f2.error_messages['custom'].text, 'changed')

def test_field_deepcopy_error_messages_value_identity_charfield(self):

    class CustomMessage:

        def __init__(self, text):
            self.text = text
    f = CharField(error_messages={'custom': CustomMessage('orig')})
    f2 = copy.deepcopy(f)
    self.assertIsNot(f2.error_messages, f.error_messages)
    self.assertIs(f2.error_messages['custom'], f.error_messages['custom'])
    f.error_messages['custom'].text = 'mutated'
    self.assertEqual(f2.error_messages['custom'].text, 'mutated')

def test_field_deepcopy_error_messages_value_identity_datefield(self):

    class CustomMessage:

        def __init__(self, value):
            self.value = value
    f = DateField(error_messages={'custom_date': CustomMessage(123)})
    f2 = copy.deepcopy(f)
    self.assertIsNot(f2.error_messages, f.error_messages)
    self.assertIs(f2.error_messages['custom_date'], f.error_messages['custom_date'])
    f.error_messages['custom_date'].value = 999
    self.assertEqual(f2.error_messages['custom_date'].value, 999)

def test_field_deepcopy_error_messages_value_identity_multivaluefield(self):

    class CustomMessage:

        def __init__(self, s):
            self.s = s

    class DummyMulti(MultiValueField):

        def __init__(self, **kwargs):
            fields = (CharField(), CharField())
            super().__init__(fields=fields, **kwargs)

        def compress(self, data_list):
            return data_list
    f = DummyMulti(error_messages={'custom': CustomMessage('a')})
    f2 = copy.deepcopy(f)
    self.assertIsNot(f2.error_messages, f.error_messages)
    self.assertIs(f2.error_messages['custom'], f.error_messages['custom'])
    f.error_messages['custom'].s = 'b'
    self.assertEqual(f2.error_messages['custom'].s, 'b')

def test_field_deepcopy_error_messages_value_identity_imagefield(self):

    class CustomMessage:

        def __init__(self, msg):
            self.msg = msg
    f = ImageField(error_messages={'invalid_image': CustomMessage('img')})
    f2 = copy.deepcopy(f)
    self.assertIsNot(f2.error_messages, f.error_messages)
    self.assertIs(f2.error_messages['invalid_image'], f.error_messages['invalid_image'])
    f.error_messages['invalid_image'].msg = 'changed-img'
    self.assertEqual(f2.error_messages['invalid_image'].msg, 'changed-img')

def test_field_deepcopy_error_messages_value_identity_choicefield(self):

    class CustomMessage:

        def __init__(self, n):
            self.n = n
    f = ChoiceField(choices=[('A', 'A')], error_messages={'custom': CustomMessage(1)})
    f2 = copy.deepcopy(f)
    self.assertIsNot(f2.error_messages, f.error_messages)
    self.assertIs(f2.error_messages['custom'], f.error_messages['custom'])
    f.error_messages['custom'].n = 2
    self.assertEqual(f2.error_messages['custom'].n, 2)

def test_field_deepcopy_error_messages_value_identity_typedchoicefield(self):

    class CustomMessage:

        def __init__(self, tag):
            self.tag = tag
    f = TypedChoiceField(choices=[('1', 'One')], coerce=int, error_messages={'custom': CustomMessage('x')})
    f2 = copy.deepcopy(f)
    self.assertIsNot(f2.error_messages, f.error_messages)
    self.assertIs(f2.error_messages['custom'], f.error_messages['custom'])
    f.error_messages['custom'].tag = 'y'
    self.assertEqual(f2.error_messages['custom'].tag, 'y')

def test_field_deepcopy_error_messages_value_identity_multiplechoicefield(self):

    class CustomMessage:

        def __init__(self, payload):
            self.payload = payload
    f = MultipleChoiceField(choices=[('A', 'A')], error_messages={'custom_list': CustomMessage([1, 2])})
    f2 = copy.deepcopy(f)
    self.assertIsNot(f2.error_messages, f.error_messages)
    self.assertIs(f2.error_messages['custom_list'], f.error_messages['custom_list'])
    f.error_messages['custom_list'].payload.append(3)
    self.assertEqual(f2.error_messages['custom_list'].payload, [1, 2, 3])

def test_field_deepcopy_error_messages_value_identity_uuidfield(self):

    class CustomMessage:

        def __init__(self, data):
            self.data = data
    f = UUIDField(error_messages={'invalid': CustomMessage('u')})
    f2 = copy.deepcopy(f)
    self.assertIsNot(f2.error_messages, f.error_messages)
    self.assertIs(f2.error_messages['invalid'], f.error_messages['invalid'])
    f.error_messages['invalid'].data = 'updated'
    self.assertEqual(f2.error_messages['invalid'].data, 'updated')

def test_field_deepcopy_error_messages_value_identity_regexfield(self):

    class CustomMessage:

        def __init__(self, v):
            self.v = v
    f = RegexField(regex='.*', error_messages={'custom': CustomMessage('z')})
    f2 = copy.deepcopy(f)
    self.assertIsNot(f2.error_messages, f.error_messages)
    self.assertIs(f2.error_messages['custom'], f.error_messages['custom'])
    f.error_messages['custom'].v = 'zz'
    self.assertEqual(f2.error_messages['custom'].v, 'zz')

def test_deepcopy_error_messages_shares_nested_custom_object_on_field(self):

    class MutObj:

        def __init__(self, value):
            self.value = value
    f = CharField(error_messages={'custom': MutObj('orig')})
    f_copy = copy.deepcopy(f)
    self.assertIsNot(f_copy.error_messages, f.error_messages)
    f.error_messages['custom'].value = 'changed'
    self.assertEqual(f_copy.error_messages['custom'].value, 'changed')

def test_deepcopy_error_messages_shares_nested_list_value_on_field(self):
    f = CharField(error_messages={'custom_list': ['one']})
    f_copy = copy.deepcopy(f)
    self.assertIsNot(f_copy.error_messages, f.error_messages)
    f.error_messages['custom_list'].append('two')
    self.assertEqual(f_copy.error_messages['custom_list'], ['one', 'two'])

def test_deepcopy_error_messages_shares_nested_dict_value_on_field(self):
    f = CharField(error_messages={'custom_dict': {'k': 'v'}})
    f_copy = copy.deepcopy(f)
    self.assertIsNot(f_copy.error_messages, f.error_messages)
    f.error_messages['custom_dict']['new'] = 'x'
    self.assertIn('new', f_copy.error_messages['custom_dict'])
    self.assertEqual(f_copy.error_messages['custom_dict']['new'], 'x')

def test_deepcopy_nested_mutation_via_copy_reflects_in_original(self):

    class MutObj:

        def __init__(self, value):
            self.value = value
    f = CharField(error_messages={'obj': MutObj('a')})
    f_copy = copy.deepcopy(f)
    f_copy.error_messages['obj'].value = 'modified-via-copy'
    self.assertEqual(f.error_messages['obj'].value, 'modified-via-copy')

def test_deepcopy_error_messages_shallow_on_form_field(self):

    class MutObj:

        def __init__(self, value):
            self.value = value

    class SimpleForm(Form):
        name = CharField(error_messages={'nested': MutObj('orig')})
    form1 = SimpleForm()
    form2 = copy.deepcopy(form1)
    form1.fields['name'].error_messages['nested'].value = 'changed'
    self.assertEqual(form2.fields['name'].error_messages['nested'].value, 'changed')

def test_deepcopy_error_messages_shares_list_nested_on_form_field(self):

    class SimpleForm(Form):
        name = CharField(error_messages={'nested_list': ['x']})
    form1 = SimpleForm()
    form2 = copy.deepcopy(form1)
    form1.fields['name'].error_messages['nested_list'].append('y')
    self.assertEqual(form2.fields['name'].error_messages['nested_list'], ['x', 'y'])

def test_deepcopy_error_messages_shares_dict_nested_on_form_field(self):

    class SimpleForm(Form):
        name = CharField(error_messages={'nested_dict': {'a': 1}})
    form1 = SimpleForm()
    form2 = copy.deepcopy(form1)
    form1.fields['name'].error_messages['nested_dict']['b'] = 2
    self.assertEqual(form2.fields['name'].error_messages['nested_dict']['b'], 2)

def test_deepcopy_error_messages_shallow_with_custom_field_subclass(self):

    class MutObj:

        def __init__(self, value):
            self.value = value

    class CustomField(CharField):

        def __init__(self, **kwargs):
            kwargs.setdefault('error_messages', {})
            kwargs['error_messages'].setdefault('mut', MutObj('init'))
            super().__init__(**kwargs)
    f = CustomField()
    f_copy = copy.deepcopy(f)
    f.error_messages['mut'].value = 'changed-subclass'
    self.assertEqual(f_copy.error_messages['mut'].value, 'changed-subclass')

def test_deepcopy_error_messages_mapping_independent_at_top_level(self):

    class MutObj:

        def __init__(self, value):
            self.value = value
    f = CharField(error_messages={'k': MutObj('v')})
    f_copy = copy.deepcopy(f)
    f.error_messages['k'] = MutObj('new')
    self.assertEqual(f_copy.error_messages['k'].value, 'v')

def test_deepcopy_error_messages_shared_nested_for_multivaluefield(self):

    class MutObj:

        def __init__(self, value):
            self.value = value

    class MVField(MultiValueField):

        def __init__(self, **kwargs):
            fields = (CharField(), CharField())
            kwargs.setdefault('error_messages', {})
            kwargs['error_messages'].setdefault('mut', MutObj('m'))
            super().__init__(fields=fields, **kwargs)

        def compress(self, data_list):
            return '-'.join(data_list)
    f = MVField()
    f_copy = copy.deepcopy(f)
    f.error_messages['mut'].value = 'modified-mv'
    self.assertEqual(f_copy.error_messages['mut'].value, 'modified-mv')

import copy
from django.forms import CharField, Field, Form
from django.test import SimpleTestCase

class FieldDeepcopyNestedTests(SimpleTestCase):

    def test_field_deepcopy_shared_nested_list(self):
        f = CharField(error_messages={'mut': ['orig']})
        f2 = copy.deepcopy(f)
        self.assertIsNot(f.error_messages, f2.error_messages)
        self.assertIs(f.error_messages['mut'], f2.error_messages['mut'])
        f.error_messages['mut'].append('changed')
        self.assertIn('changed', f2.error_messages['mut'])

    def test_field_deepcopy_shared_nested_dict(self):
        nested = {'inner': ['a']}
        f = CharField(error_messages={'mut': nested})
        f2 = copy.deepcopy(f)
        self.assertIsNot(f.error_messages, f2.error_messages)
        self.assertIs(f.error_messages['mut'], f2.error_messages['mut'])
        f.error_messages['mut']['inner'].append('b')
        self.assertIn('b', f2.error_messages['mut']['inner'])

    def test_field_deepcopy_shared_mutable_custom_object(self):

        class Mutable:

            def __init__(self, val):
                self.val = val

            def __repr__(self):
                return f'Mutable({self.val!r})'
        m = Mutable('orig')
        f = CharField(error_messages={'mut': m})
        f2 = copy.deepcopy(f)
        self.assertIsNot(f.error_messages, f2.error_messages)
        self.assertIs(f.error_messages['mut'], f2.error_messages['mut'])
        f.error_messages['mut'].val = 'changed'
        self.assertEqual(f2.error_messages['mut'].val, 'changed')

    def test_form_field_deepcopy_shared_nested_list(self):

        class MyForm(Form):
            name = CharField(error_messages={'mut': ['orig']})
        f1 = MyForm()
        f2 = MyForm()
        self.assertIsNot(f1.fields['name'].error_messages, f2.fields['name'].error_messages)
        self.assertIs(f1.fields['name'].error_messages['mut'], f2.fields['name'].error_messages['mut'])
        f1.fields['name'].error_messages['mut'].append('x')
        self.assertIn('x', f2.fields['name'].error_messages['mut'])

    def test_form_field_deepcopy_shared_nested_dict(self):

        class MyForm(Form):
            name = CharField(error_messages={'mut': {'inner': ['a']}})
        f1 = MyForm()
        f2 = MyForm()
        self.assertIsNot(f1.fields['name'].error_messages, f2.fields['name'].error_messages)
        self.assertIs(f1.fields['name'].error_messages['mut'], f2.fields['name'].error_messages['mut'])
        f1.fields['name'].error_messages['mut']['inner'].append('b')
        self.assertIn('b', f2.fields['name'].error_messages['mut']['inner'])

    def test_form_field_deepcopy_shared_mutable_custom_object(self):

        class Mutable:

            def __init__(self, val):
                self.val = val

        class MyForm(Form):
            name = CharField(error_messages={'mut': Mutable('orig')})
        f1 = MyForm()
        f2 = MyForm()
        self.assertIsNot(f1.fields['name'].error_messages, f2.fields['name'].error_messages)
        self.assertIs(f1.fields['name'].error_messages['mut'], f2.fields['name'].error_messages['mut'])
        f1.fields['name'].error_messages['mut'].val = 'changed'
        self.assertEqual(f2.fields['name'].error_messages['mut'].val, 'changed')

def _make_custom_obj(value):

    class CustomObject:

        def __init__(self, value):
            self.value = value

        def __repr__(self):
            return 'CustomObject(%r)' % (self.value,)
    return CustomObject(value)

def test_field_deepcopy_shares_nested_error_messages_value_charfield(self):
    obj = _make_custom_obj('original')
    f = CharField(error_messages={'custom': obj})
    f_copy = copy.deepcopy(f)
    self.assertIsNot(f_copy.error_messages, f.error_messages)
    self.assertIs(f_copy.error_messages['custom'], f.error_messages['custom'])
    f.error_messages['custom'].value = 'modified'
    self.assertEqual(f_copy.error_messages['custom'].value, 'modified')

def test_field_deepcopy_shares_nested_error_messages_value_integerfield(self):
    obj = _make_custom_obj('int-orig')
    f = IntegerField(error_messages={'custom': obj})
    f_copy = copy.deepcopy(f)
    self.assertIsNot(f_copy.error_messages, f.error_messages)
    self.assertIs(f_copy.error_messages['custom'], f.error_messages['custom'])
    f.error_messages['custom'].value = 'int-modified'
    self.assertEqual(f_copy.error_messages['custom'].value, 'int-modified')

def test_field_deepcopy_shares_nested_error_messages_value_choicefield(self):
    obj = _make_custom_obj('choice-orig')
    f = ChoiceField(error_messages={'custom': obj}, choices=[])
    f_copy = copy.deepcopy(f)
    self.assertIsNot(f_copy.error_messages, f.error_messages)
    self.assertIs(f_copy.error_messages['custom'], f.error_messages['custom'])
    f.error_messages['custom'].value = 'choice-mod'
    self.assertEqual(f_copy.error_messages['custom'].value, 'choice-mod')

def test_multivaluefield_deepcopy_shares_nested_error_messages_value(self):
    obj = _make_custom_obj('multi-orig')

    class SimpleMultiField(MultiValueField):

        def __init__(self, *args, **kwargs):
            fields = (CharField(), CharField())
            super().__init__(fields=fields, **kwargs)

        def compress(self, data_list):
            return ','.join(data_list)
    f = SimpleMultiField(error_messages={'custom': obj})
    f_copy = copy.deepcopy(f)
    self.assertIsNot(f_copy.error_messages, f.error_messages)
    self.assertIs(f_copy.error_messages['custom'], f.error_messages['custom'])
    f.error_messages['custom'].value = 'multi-mod'
    self.assertEqual(f_copy.error_messages['custom'].value, 'multi-mod')

def test_form_deepcopy_shares_field_error_messages_value(self):
    obj = _make_custom_obj('form-orig')

    class ProfileForm(Form):
        name = CharField(error_messages={'custom': obj})
    form = ProfileForm()
    form_copy = copy.deepcopy(form)
    self.assertIsNot(form_copy.fields['name'], form.fields['name'])
    self.assertIsNot(form_copy.fields['name'].error_messages, form.fields['name'].error_messages)
    self.assertIs(form_copy.fields['name'].error_messages['custom'], form.fields['name'].error_messages['custom'])
    form.fields['name'].error_messages['custom'].value = 'form-mod'
    self.assertEqual(form_copy.fields['name'].error_messages['custom'].value, 'form-mod')

def test_form_deepcopy_preserves_shared_object_between_fields(self):
    shared = _make_custom_obj('shared-orig')

    class ShareForm(Form):
        a = CharField(error_messages={'info': shared})
        b = CharField(error_messages={'info': shared})
    f = ShareForm()
    f_copy = copy.deepcopy(f)
    self.assertIs(f_copy.fields['a'].error_messages['info'], f_copy.fields['b'].error_messages['info'])
    f.fields['a'].error_messages['info'].value = 'shared-mod'
    self.assertEqual(f_copy.fields['a'].error_messages['info'].value, 'shared-mod')
    self.assertEqual(f_copy.fields['b'].error_messages['info'].value, 'shared-mod')

def test_multifield_in_form_deepcopy_shares_nested_error_messages_value(self):
    obj = _make_custom_obj('form-multi-orig')

    class DateAgeField(MultiValueField):

        def __init__(self, *args, **kwargs):
            fields = (DateField(), IntegerField())
            super().__init__(fields=fields, **kwargs)

        def compress(self, data_list):
            return tuple(data_list)

    class F(Form):
        date_age = DateAgeField(error_messages={'custom': obj})
    form = F()
    form_copy = copy.deepcopy(form)
    self.assertIsNot(form_copy.fields['date_age'].error_messages, form.fields['date_age'].error_messages)
    self.assertIs(form_copy.fields['date_age'].error_messages['custom'], form.fields['date_age'].error_messages['custom'])
    form.fields['date_age'].error_messages['custom'].value = 'form-multi-mod'
    self.assertEqual(form_copy.fields['date_age'].error_messages['custom'].value, 'form-multi-mod')

def test_choicefield_in_form_deepcopy_shares_nested_error_messages_value(self):
    obj = _make_custom_obj('form-choice-orig')

    class F(Form):
        lang = ChoiceField(choices=[('P', 'Python')], error_messages={'custom': obj})
    form = F()
    form_copy = copy.deepcopy(form)
    self.assertIsNot(form_copy.fields['lang'].error_messages, form.fields['lang'].error_messages)
    self.assertIs(form_copy.fields['lang'].error_messages['custom'], form.fields['lang'].error_messages['custom'])
    form.fields['lang'].error_messages['custom'].value = 'form-choice-mod'
    self.assertEqual(form_copy.fields['lang'].error_messages['custom'].value, 'form-choice-mod')

def test_field_deepcopy_preserves_value_identity_custom_object(self):

    class CustomMessage:

        def __init__(self, text):
            self.text = text
    field = CharField(error_messages={'custom': CustomMessage('orig')})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom'], field.error_messages['custom'])

def test_field_deepcopy_value_mutation_reflects_in_copy_custom_object(self):

    class CustomMessage:

        def __init__(self, text):
            self.text = text
    field = CharField(error_messages={'custom': CustomMessage('orig')})
    field_copy = copy.deepcopy(field)
    field.error_messages['custom'].text = 'modified'
    self.assertEqual(field_copy.error_messages['custom'].text, 'modified')

def test_field_deepcopy_preserves_value_identity_list(self):
    shared_list = [1, 2, 3]
    field = CharField(error_messages={'custom': shared_list})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom'], field.error_messages['custom'])
    field.error_messages['custom'].append(4)
    self.assertEqual(field_copy.error_messages['custom'][-1], 4)

def test_field_deepcopy_preserves_value_identity_dict(self):
    shared_dict = {'a': 1}
    field = CharField(error_messages={'custom': shared_dict})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom'], field.error_messages['custom'])
    field.error_messages['custom']['b'] = 2
    self.assertIn('b', field_copy.error_messages['custom'])

def test_form_deepcopy_preserves_field_error_message_identity(self):

    class CustomMessage:

        def __init__(self, text):
            self.text = text

    class SampleForm(Form):
        name = CharField(error_messages={'custom': CustomMessage('orig')})
    form = SampleForm()
    form_copy = copy.deepcopy(form)
    self.assertIsNot(form_copy.fields['name'].error_messages, form.fields['name'].error_messages)
    self.assertIs(form_copy.fields['name'].error_messages['custom'], form.fields['name'].error_messages['custom'])

def test_form_deepcopy_value_mutation_reflects_in_copy(self):

    class CustomMessage:

        def __init__(self, text):
            self.text = text

    class SampleForm(Form):
        name = CharField(error_messages={'custom': CustomMessage('orig')})
    form = SampleForm()
    form_copy = copy.deepcopy(form)
    form.fields['name'].error_messages['custom'].text = 'mutated'
    self.assertEqual(form_copy.fields['name'].error_messages['custom'].text, 'mutated')

def test_charfield_deepcopy_preserves_value_identity_exception_instance(self):
    ex = ValueError('boom')
    field = CharField(error_messages={'custom': ex})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom'], field.error_messages['custom'])
    field.error_messages['custom'].args = ('boom2',)
    self.assertEqual(field_copy.error_messages['custom'].args[0], 'boom2')

def test_field_deepcopy_preserves_value_identity_multiple_keys_same_object(self):
    shared_obj = object()
    field = CharField(error_messages={'a': shared_obj, 'b': shared_obj})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['a'], field.error_messages['a'])
    self.assertIs(field_copy.error_messages['b'], field.error_messages['b'])
    self.assertIs(field_copy.error_messages['a'], field_copy.error_messages['b'])

def test_field_deepcopy_preserves_value_identity_for_callable_like(self):

    class CallableObj:

        def __call__(self):
            return 'called'
    c = CallableObj()
    field = CharField(error_messages={'callable': c})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['callable'], field.error_messages['callable'])

None
import copy
import datetime
from django.forms import CharField, Form, Field
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

class FormsTestCaseFieldErrorMessagesShallowCopy(SimpleTestCase):
    def test_deepcopy_preserves_custom_object_value_reference(self):
        class CustomObject:
            def __init__(self, value):
                self.value = value
            def __repr__(self):
                return "CustomObject(%r)" % (self.value,)

        f = CharField(error_messages={'custom': CustomObject('orig')})
        f_copy = copy.deepcopy(f)

        # The dict object should be different
        self.assertIsNot(f_copy.error_messages, f.error_messages)
        # But the value stored under the key should be the same object (shallow copy).
        self.assertIs(f_copy.error_messages['custom'], f.error_messages['custom'])

        # Mutate original nested object and ensure copy sees the change (shared value)
        f.error_messages['custom'].value = 'changed'
        self.assertEqual(f_copy.error_messages['custom'].value, 'changed')

    def test_deepcopy_preserves_list_value_reference(self):
        f = CharField(error_messages={'alist': [1, 2]})
        f_copy = copy.deepcopy(f)
        self.assertIsNot(f_copy.error_messages, f.error_messages)
        # The list object should be the same (shallow copy semantics)
        self.assertIs(f_copy.error_messages['alist'], f.error_messages['alist'])

        # Mutate original list
        f.error_messages['alist'].append(3)
        self.assertEqual(f_copy.error_messages['alist'], [1, 2, 3])

    def test_deepcopy_preserves_nested_dict_reference(self):
        nested = {'inner': 'v'}
        f = CharField(error_messages={'d': nested})
        f_copy = copy.deepcopy(f)
        self.assertIsNot(f_copy.error_messages, f.error_messages)
        # The nested dict object should be the same object
        self.assertIs(f_copy.error_messages['d'], f.error_messages['d'])

        # Mutate nested dict
        nested['inner'] = 'changed'
        self.assertEqual(f_copy.error_messages['d']['inner'], 'changed')

    def test_deepcopy_preserves_shared_value_identity_across_keys(self):
        shared = []
        f = CharField(error_messages={'a': shared, 'b': shared})
        f_copy = copy.deepcopy(f)
        self.assertIsNot(f_copy.error_messages, f.error_messages)
        # Both keys should still reference the same object in the copy
        self.assertIs(f_copy.error_messages['a'], f_copy.error_messages['b'])
        # And that object should be the same as the original shared object
        self.assertIs(f_copy.error_messages['a'], shared)

        # Mutate through original
        shared.append('x')
        self.assertIn('x', f_copy.error_messages['a'])

    def test_deepcopy_reflects_mutation_for_form_field(self):
        class CustomForm(Form):
            name = CharField(error_messages={'custom': {'msg': ['ok']}})

        form = CustomForm()
        form_copy = copy.deepcopy(form)

        orig_em = form.fields['name'].error_messages
        copy_em = form_copy.fields['name'].error_messages
        self.assertIsNot(copy_em, orig_em)
        # But the nested list should be the same object
        self.assertIs(copy_em['custom']['msg'], orig_em['custom']['msg'])

        # Mutate original nested list
        orig_em['custom']['msg'].append('added')
        self.assertIn('added', copy_em['custom']['msg'])

    def test_deepcopy_preserves_list_mutation_reflected_in_copy_for_form_field(self):
        class CustomForm(Form):
            age = CharField(error_messages={'a': [0]})

        form = CustomForm()
        form_copy = copy.deepcopy(form)

        orig = form.fields['age'].error_messages
        copyem = form_copy.fields['age'].error_messages
        self.assertIsNot(orig, copyem)
        self.assertIs(orig['a'], copyem['a'])

        orig['a'].extend([1,2])
        self.assertEqual(copyem['a'], [0,1,2])

    def test_deepcopy_preserves_mutable_in_error_messages_after_field_copy(self):
        class MutableThing:
            def __init__(self, data):
                self.data = data
            def append(self, v):
                self.data.append(v)

        mt = MutableThing([1])
        f = CharField(error_messages={'mt': mt})
        f_copy = copy.deepcopy(f)
        self.assertIs(f_copy.error_messages['mt'], mt)
        # Mutate original object's internal state
        mt.append(2)
        self.assertEqual(f_copy.error_messages['mt'].data, [1,2])

    def test_deepcopy_preserves_nested_list_identity(self):
        nested = [ ['a'] ]
        f = CharField(error_messages={'n': nested})
        f_copy = copy.deepcopy(f)
        self.assertIs(f_copy.error_messages['n'][0], nested[0])
        # Mutate the inner list
        nested[0].append('b')
        self.assertEqual(f_copy.error_messages['n'][0], ['a','b'])

    def test_deepcopy_preserves_shared_mutable_across_fields_in_form(self):
        shared = {'k': 1}
        class MyForm(Form):
            f1 = CharField(error_messages={'x': shared})
            f2 = CharField(error_messages={'y': shared})

        form = MyForm()
        form_copy = copy.deepcopy(form)
        f1_em = form.fields['f1'].error_messages
        f2_em = form.fields['f2'].error_messages
        f1_copy_em = form_copy.fields['f1'].error_messages
        f2_copy_em = form_copy.fields['f2'].error_messages

        # Ensure the copy's two fields still share the same nested object
        self.assertIs(f1_copy_em['x'], f2_copy_em['y'])
        # And that object is the same as the original shared object
        self.assertIs(f1_copy_em['x'], shared)

        # Mutate original shared object
        shared['k'] = 99
        self.assertEqual(f1_copy_em['x']['k'], 99)

    def test_deepcopy_shallow_for_multiple_deep_levels(self):
        inner = {'v': [0]}
        f = CharField(error_messages={'lvl1': inner})
        f_copy = copy.deepcopy(f)
        # inner should be same object reference
        self.assertIs(f_copy.error_messages['lvl1'], inner)
        inner['v'].append(1)
        self.assertEqual(f_copy.error_messages['lvl1']['v'], [0,1])

# No new imports needed; reuses imports already present in the test module.
import copy

from django.forms import CharField, ChoiceField, Form
from django.test import SimpleTestCase
from django.core.exceptions import ValidationError


class FieldErrorMessagesShallowCopyTests(SimpleTestCase):
    def test_field_deepcopy_shared_custom_object_mutation_reflected(self):
        class CustomMsg:
            def __init__(self, value):
                self.value = value

            def __repr__(self):
                return "CustomMsg(%r)" % (self.value,)

        f = CharField()
        # Set error_messages to include a mutable custom object
        f.error_messages = {'custom': CustomMsg('original')}
        f_copy = copy.deepcopy(f)

        # The dicts should be different objects
        self.assertIsNot(f_copy.error_messages, f.error_messages)
        # But the nested custom object should be the same reference (shallow copy)
        self.assertIs(f_copy.error_messages['custom'], f.error_messages['custom'])

        # Mutate the nested object on the original and verify the copy sees it
        f.error_messages['custom'].value = 'modified'
        self.assertEqual(f_copy.error_messages['custom'].value, 'modified')

    def test_field_deepcopy_shared_list_mutation_reflected(self):
        f = CharField()
        f.error_messages = {'custom': ['one']}
        f_copy = copy.deepcopy(f)

        self.assertIsNot(f_copy.error_messages, f.error_messages)
        # The nested list should be shared
        self.assertIs(f_copy.error_messages['custom'], f.error_messages['custom'])

        f.error_messages['custom'].append('two')
        self.assertEqual(f_copy.error_messages['custom'], ['one', 'two'])

    def test_form_deepcopy_shared_custom_object_mutation_reflected(self):
        class CustomMsg:
            def __init__(self, value):
                self.value = value

        class SampleForm(Form):
            name = CharField()

        form = SampleForm()
        form.fields['name'].error_messages = {'custom': CustomMsg('orig')}
        form_copy = copy.deepcopy(form)

        self.assertIsNot(form_copy.fields['name'].error_messages, form.fields['name'].error_messages)
        # Nested object must be the same reference
        self.assertIs(form_copy.fields['name'].error_messages['custom'],
                      form.fields['name'].error_messages['custom'])

        form.fields['name'].error_messages['custom'].value = 'changed'
        self.assertEqual(form_copy.fields['name'].error_messages['custom'].value, 'changed')

    def test_form_deepcopy_shared_list_mutation_reflected(self):
        class SampleForm(Form):
            name = CharField()

        form = SampleForm()
        form.fields['name'].error_messages = {'custom': ['a']}
        form_copy = copy.deepcopy(form)

        self.assertIsNot(form_copy.fields['name'].error_messages, form.fields['name'].error_messages)
        self.assertIs(form_copy.fields['name'].error_messages['custom'],
                      form.fields['name'].error_messages['custom'])

        form.fields['name'].error_messages['custom'].append('b')
        self.assertEqual(form_copy.fields['name'].error_messages['custom'], ['a', 'b'])

    def test_deepcopy_two_fields_sharing_same_mutable_object_reflection(self):
        class CustomMsg:
            def __init__(self, value):
                self.value = value

        class SampleForm(Form):
            a = CharField()
            b = CharField()

        shared = CustomMsg('shared_orig')
        form = SampleForm()
        # Both fields reference the same mutable object inside their error_messages
        form.fields['a'].error_messages = {'custom': shared}
        form.fields['b'].error_messages = {'custom': shared}

        form_copy = copy.deepcopy(form)

        # Ensure the two error_messages dicts themselves are different objects on the copy
        self.assertIsNot(form_copy.fields['a'].error_messages, form.fields['a'].error_messages)
        self.assertIsNot(form_copy.fields['b'].error_messages, form.fields['b'].error_messages)

        # But the nested shared object should be the same reference in the copy as in the original
        self.assertIs(form_copy.fields['a'].error_messages['custom'],
                      form.fields['a'].error_messages['custom'])
        self.assertIs(form_copy.fields['b'].error_messages['custom'],
                      form.fields['b'].error_messages['custom'])

        # Changing the nested object via original should be reflected in the copy
        shared.value = 'mutated'
        self.assertEqual(form_copy.fields['a'].error_messages['custom'].value, 'mutated')
        self.assertEqual(form_copy.fields['b'].error_messages['custom'].value, 'mutated')

    def test_field_deepcopy_shallow_copy_preserves_nested_dict_mutation(self):
        f = CharField()
        nested = {'k': 'v'}
        f.error_messages = {'custom': nested}
        f_copy = copy.deepcopy(f)

        self.assertIsNot(f_copy.error_messages, f.error_messages)
        # nested dict should be the same reference
        self.assertIs(f_copy.error_messages['custom'], nested)
        # mutate nested dict
        nested['k'] = 'changed'
        self.assertEqual(f_copy.error_messages['custom']['k'], 'changed')

    def test_field_with_class_default_error_messages_mutable_list_shared(self):
        # Create a field subclass that defines default_error_messages with a mutable list
        class MyField(CharField):
            default_error_messages = {'x': ['one']}

        f = MyField()
        # Instance built error_messages will reference the class-level list object
        # (update() copies the reference).
        f_copy = copy.deepcopy(f)

        # The dicts must be different
        self.assertIsNot(f_copy.error_messages, f.error_messages)
        # But the nested list should still be the same object (shallow copy)
        self.assertIs(f_copy.error_messages['x'], f.error_messages['x'])

        # Mutate the list and verify copy sees change
        f.error_messages['x'].append('two')
        self.assertEqual(f_copy.error_messages['x'], ['one', 'two'])

    def test_form_deepcopy_field_with_class_default_error_messages_mutable_list_shared(self):
        class MyField(CharField):
            default_error_messages = {'x': ['foo']}

        class SampleForm(Form):
            f = MyField()

        form = SampleForm()
        form_copy = copy.deepcopy(form)

        self.assertIsNot(form_copy.fields['f'].error_messages, form.fields['f'].error_messages)
        self.assertIs(form_copy.fields['f'].error_messages['x'],
                      form.fields['f'].error_messages['x'])

        form.fields['f'].error_messages['x'].append('bar')
        self.assertEqual(form_copy.fields['f'].error_messages['x'], ['foo', 'bar'])

    def test_deepcopy_preserves_shared_mutable_nested_structures(self):
        # Error messages value is a nested mutable structure (dict containing list)
        nested = {'lst': [1]}
        f = CharField()
        f.error_messages = {'complex': nested}
        f_copy = copy.deepcopy(f)

        self.assertIsNot(f_copy.error_messages, f.error_messages)
        # Nested structure reference is shared (shallow copy)
        self.assertIs(f_copy.error_messages['complex'], nested)

        nested['lst'].append(2)
        self.assertEqual(f_copy.error_messages['complex']['lst'], [1, 2])

# No new imports required; tests rely on existing imports in the tests file.
import copy
import datetime
import json
import uuid

from django.core.exceptions import NON_FIELD_ERRORS
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import MaxValueValidator, RegexValidator
from django.forms import (
    BooleanField, CharField, CheckboxSelectMultiple, ChoiceField, DateField,
    DateTimeField, EmailField, FileField, FloatField, Form, HiddenInput,
    ImageField, IntegerField, MultipleChoiceField, MultipleHiddenInput,
    MultiValueField, NullBooleanField, PasswordInput, RadioSelect, Select,
    SplitDateTimeField, SplitHiddenDateTimeWidget, Textarea, TextInput,
    TimeField, ValidationError, forms,
)
from django.forms.renderers import DjangoTemplates, get_default_renderer
from django.forms.utils import ErrorList
from django.http import QueryDict
from django.template import Context, Template
from django.test import SimpleTestCase
from django.utils.datastructures import MultiValueDict
from django.utils.safestring import mark_safe

# The repository's tests file already contains many tests. We add the new regression
# tests to the existing FormsTestCase below.

class FormsTestCase(SimpleTestCase):
    # ... existing tests in the file (omitted here) ...

    # New regression tests for Field.__deepcopy__ behavior (error_messages handling).
    def test_field_deepcopy_shares_inner_mutable_error_message_object(self):
        """
        When deep-copying a Field, error_messages dict should be shallow-copied:
        the dict object is new, but inner mutable objects are the same instances.
        """
        class CustomMsg:
            def __init__(self, txt):
                self.txt = txt
            def __repr__(self):
                return "CustomMsg(%r)" % (self.txt,)

        field = CharField(error_messages={'custom': CustomMsg('original')})
        field_copy = copy.deepcopy(field)
        # The dict itself should be a different object
        self.assertIsNot(field_copy.error_messages, field.error_messages)
        # But the inner custom object should be the same instance (shallow copy)
        self.assertIs(field_copy.error_messages['custom'], field.error_messages['custom'])
        # Mutating original inner object should be visible in the copy
        field.error_messages['custom'].txt = 'modified'
        self.assertEqual(field_copy.error_messages['custom'].txt, 'modified')

    def test_form_deepcopy_shares_inner_mutable_error_message_object(self):
        """
        Deep-copying a Form should result in fields whose error_messages inner
        objects are shared (shallow copy semantics for the inner objects).
        """
        class CustomMsg:
            def __init__(self, txt):
                self.txt = txt
            def __repr__(self):
                return "CustomMsg(%r)" % (self.txt,)

        class F(Form):
            name = CharField(error_messages={'custom': CustomMsg('orig')})

        f1 = F()
        f2 = copy.deepcopy(f1)
        self.assertIsNot(f2.fields['name'].error_messages, f1.fields['name'].error_messages)
        # inner object shared
        self.assertIs(f2.fields['name'].error_messages['custom'], f1.fields['name'].error_messages['custom'])
        f1.fields['name'].error_messages['custom'].txt = 'changed'
        self.assertEqual(f2.fields['name'].error_messages['custom'].txt, 'changed')

    def test_field_deepcopy_shares_inner_mutable_error_message_list(self):
        """
        If an error_messages value is a mutable list, the deepcopy of the Field
        should share that list (shallow copy of values).
        """
        field = CharField(error_messages={'custom': ['one']})
        field_copy = copy.deepcopy(field)
        self.assertIsNot(field_copy.error_messages, field.error_messages)
        # list object should be identical under shallow-copy semantics
        self.assertIs(field_copy.error_messages['custom'], field.error_messages['custom'])
        field.error_messages['custom'].append('two')
        self.assertIn('two', field_copy.error_messages['custom'])

    def test_form_deepcopy_shares_inner_mutable_error_message_list(self):
        class F(Form):
            name = CharField(error_messages={'custom': ['a']})

        f1 = F()
        f2 = copy.deepcopy(f1)
        self.assertIsNot(f2.fields['name'].error_messages, f1.fields['name'].error_messages)
        self.assertIs(f2.fields['name'].error_messages['custom'], f1.fields['name'].error_messages['custom'])
        f1.fields['name'].error_messages['custom'].append('b')
        self.assertIn('b', f2.fields['name'].error_messages['custom'])

    def test_field_deepcopy_shares_inner_mutable_error_message_nested_dict(self):
        """
        Nested dict inside error_messages should be shared (shallow inner copy).
        """
        nested = {'inner': {'k': 'v'}}
        field = CharField(error_messages={'custom': nested})
        field_copy = copy.deepcopy(field)
        self.assertIsNot(field_copy.error_messages, field.error_messages)
        # nested dict should be same object under shallow semantics
        self.assertIs(field_copy.error_messages['custom'], field.error_messages['custom'])
        field.error_messages['custom']['inner']['k'] = 'changed'
        self.assertEqual(field_copy.error_messages['custom']['inner']['k'], 'changed')

    def test_form_deepcopy_shares_inner_mutable_error_message_nested_dict(self):
        nested = {'x': {'y': 1}}
        class F(Form):
            name = CharField(error_messages={'custom': nested})

        f1 = F()
        f2 = copy.deepcopy(f1)
        self.assertIsNot(f2.fields['name'].error_messages, f1.fields['name'].error_messages)
        self.assertIs(f2.fields['name'].error_messages['custom'], f1.fields['name'].error_messages['custom'])
        f1.fields['name'].error_messages['custom']['x']['y'] = 2
        self.assertEqual(f2.fields['name'].error_messages['custom']['x']['y'], 2)

    def test_deepcopy_preserves_shared_inner_object_between_multiple_fields(self):
        """
        If two fields originally shared the same mutable object in error_messages,
        after deepcopy the corresponding copied fields should continue to share
        the same single inner object (shallow-copy semantics).
        """
        shared = {'msg': ['start']}
        class F(Form):
            a = CharField(error_messages={'custom': shared})
            b = CharField(error_messages={'custom': shared})

        f1 = F()
        f2 = copy.deepcopy(f1)
        a1 = f1.fields['a'].error_messages['custom']
        b1 = f1.fields['b'].error_messages['custom']
        a2 = f2.fields['a'].error_messages['custom']
        b2 = f2.fields['b'].error_messages['custom']
        # original fields share the same inner object
        self.assertIs(a1, b1)
        # copied fields should also share the same inner object (a single shared object),
        # and it should be the very same object as in the original (shallow semantics).
        self.assertIs(a2, b2)
        self.assertIs(a2, a1)
        # Mutate original shared object and observe change in copy
        a1['msg'].append('more')
        self.assertIn('more', a2['msg'])

    def test_custom_field_subclass_deepcopy_error_messages_shallow_inner(self):
        """
        A Field subclass that supplies error_messages in its __init__ should
        exhibit the same shallow-copy inner semantics on deepcopy.
        """
        class CustomChar(CharField):
            def __init__(self, **kwargs):
                kwargs.setdefault('error_messages', {})
                kwargs['error_messages'].setdefault('custom', {'val': 1})
                super().__init__(**kwargs)

        field = CustomChar()
        field_copy = copy.deepcopy(field)
        self.assertIsNot(field_copy.error_messages, field.error_messages)
        # inner dict should be the same instance
        self.assertIs(field_copy.error_messages['custom'], field.error_messages['custom'])
        field.error_messages['custom']['val'] = 99
        self.assertEqual(field_copy.error_messages['custom']['val'], 99)

def test_field_deepcopy_shares_mutable_list_charfield(self):
    lst = ['Original']
    field = CharField(error_messages={'custom': lst})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom'], lst)
    field.error_messages['custom'][0] = 'Modified'
    self.assertEqual(field_copy.error_messages['custom'][0], 'Modified')

def test_field_deepcopy_shares_mutable_dict_charfield(self):
    inner = {'msg': 'Original'}
    field = CharField(error_messages={'custom': inner})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom'], inner)
    inner['msg'] = 'Changed'
    self.assertEqual(field_copy.error_messages['custom']['msg'], 'Changed')

def test_field_deepcopy_shares_custom_object_charfield(self):

    class CustomObject:

        def __init__(self, value):
            self.value = value
    obj = CustomObject('Original')
    field = CharField(error_messages={'custom': obj})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom'], obj)
    obj.value = 'Updated'
    self.assertEqual(field_copy.error_messages['custom'].value, 'Updated')

def test_field_deepcopy_shares_list_of_custom_objects_charfield(self):

    class CustomObject:

        def __init__(self, value):
            self.value = value
    objs = [CustomObject('A'), CustomObject('B')]
    field = CharField(error_messages={'custom': objs})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom'], objs)
    objs[0].value = 'Z'
    self.assertEqual(field_copy.error_messages['custom'][0].value, 'Z')

def test_field_deepcopy_shares_nested_mutable_structure_charfield(self):
    nested = {'level1': ['one', {'inner': ['x', 'y']}]}
    field = CharField(error_messages={'custom': nested})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['custom'], nested)
    nested['level1'][1]['inner'].append('z')
    self.assertIn('z', field_copy.error_messages['custom']['level1'][1]['inner'])

def test_field_deepcopy_shares_mutable_value_in_choicefield(self):
    lst = ['OriginalChoice']
    field = ChoiceField(choices=(), error_messages={'choice_err': lst})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['choice_err'], lst)
    lst[0] = 'ChangedChoice'
    self.assertEqual(field_copy.error_messages['choice_err'][0], 'ChangedChoice')

def test_field_deepcopy_shares_mutable_value_in_filefield(self):
    lst = ['file error']
    field = FileField(error_messages={'file_err': lst})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['file_err'], lst)
    lst.append('another')
    self.assertIn('another', field_copy.error_messages['file_err'])

def test_field_deepcopy_shares_mutable_value_in_imagefield(self):
    inner = {'img': 'orig'}
    field = ImageField(error_messages={'img_err': inner})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['img_err'], inner)
    inner['img'] = 'changed'
    self.assertEqual(field_copy.error_messages['img_err']['img'], 'changed')

def test_field_deepcopy_shares_mutable_value_in_booleanfield(self):
    lst = ['must be true']
    field = BooleanField(error_messages={'bool_err': lst})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['bool_err'], lst)
    lst[0] = 'changed bool'
    self.assertEqual(field_copy.error_messages['bool_err'][0], 'changed bool')

def test_field_deepcopy_shares_mutable_value_in_integerfield(self):
    inner = {'min': 1}
    field = IntegerField(error_messages={'num_err': inner})
    field_copy = copy.deepcopy(field)
    self.assertIsNot(field_copy.error_messages, field.error_messages)
    self.assertIs(field_copy.error_messages['num_err'], inner)
    inner['min'] = 5
    self.assertEqual(field_copy.error_messages['num_err']['min'], 5)

import copy
from django.forms import CharField, Form, MultiValueField
from django.test import SimpleTestCase

class DeepCopyErrorMessagesTests(SimpleTestCase):

    def test_list_value_is_shared_between_shallow_copies(self):
        f = CharField(error_messages={'custom': ['original']})
        f_copy = copy.deepcopy(f)
        self.assertIsNot(f_copy.error_messages, f.error_messages)
        self.assertIs(f_copy.error_messages['custom'], f.error_messages['custom'])
        f.error_messages['custom'].append('modified')
        self.assertEqual(f_copy.error_messages['custom'], ['original', 'modified'])

    def test_custom_object_value_is_shared_between_shallow_copies(self):

        class CustomObj:

            def __init__(self, text):
                self.text = text

            def __repr__(self):
                return 'CustomObj(%r)' % (self.text,)
        obj = CustomObj('orig')
        f = CharField(error_messages={'obj': obj})
        f_copy = copy.deepcopy(f)
        self.assertIs(f_copy.error_messages['obj'], f.error_messages['obj'])
        f.error_messages['obj'].text = 'changed'
        self.assertEqual(f_copy.error_messages['obj'].text, 'changed')

    def test_form_field_error_messages_nested_list_shared(self):

        class NameForm(Form):
            name = CharField(error_messages={'notes': ['n']})
        form1 = NameForm()
        form2 = copy.deepcopy(form1)
        form1.fields['name'].error_messages['notes'].append('x')
        self.assertEqual(form2.fields['name'].error_messages['notes'], ['n', 'x'])
        self.assertIs(form1.fields['name'].error_messages['notes'], form2.fields['name'].error_messages['notes'])

    def test_multiple_fields_in_form_share_nested_values_after_deepcopy(self):

        class DuoForm(Form):
            a = CharField(error_messages={'l': ['a']})
            b = CharField(error_messages={'m': ['b']})
        form1 = DuoForm()
        form2 = copy.deepcopy(form1)
        form1.fields['a'].error_messages['l'].append('A2')
        form1.fields['b'].error_messages['m'].append('B2')
        self.assertEqual(form2.fields['a'].error_messages['l'], ['a', 'A2'])
        self.assertEqual(form2.fields['b'].error_messages['m'], ['b', 'B2'])

    def test_nested_dict_value_is_shared_between_shallow_copies(self):
        f = CharField(error_messages={'d': {'k': 'v'}})
        f_copy = copy.deepcopy(f)
        self.assertIs(f_copy.error_messages['d'], f.error_messages['d'])
        f.error_messages['d']['k'] = 'new'
        self.assertEqual(f_copy.error_messages['d']['k'], 'new')

    def test_multivaluefield_subfield_error_messages_share_nested_values(self):

        class PhoneField(MultiValueField):

            def __init__(self, *args, **kwargs):
                sub = CharField(error_messages={'submsg': ['ok']})
                super().__init__(*args, fields=(sub,), **kwargs)

            def compress(self, data_list):
                return data_list
        mf = PhoneField()
        mf_copy = copy.deepcopy(mf)
        self.assertIs(mf_copy.fields[0].error_messages['submsg'], mf.fields[0].error_messages['submsg'])
        mf.fields[0].error_messages['submsg'].append('added')
        self.assertEqual(mf_copy.fields[0].error_messages['submsg'], ['ok', 'added'])

    def test_modifying_copy_affects_original_for_shared_nested_objects(self):

        class Holder:

            def __init__(self, val):
                self.val = val
        obj = Holder('start')
        f = CharField(error_messages={'h': obj})
        f_copy = copy.deepcopy(f)
        f_copy.error_messages['h'].val = 'changed_via_copy'
        self.assertEqual(f.error_messages['h'].val, 'changed_via_copy')

    def test_deepcopy_on_field_preserves_mutable_value_identity_for_lists(self):
        lst = ['alpha']
        f = CharField(error_messages={'list': lst})
        f_copy = copy.deepcopy(f)
        self.assertIs(f_copy.error_messages['list'], lst)
        self.assertIs(f.error_messages['list'], lst)
        lst.append('beta')
        self.assertEqual(f_copy.error_messages['list'], ['alpha', 'beta'])

    def test_deepcopy_on_field_preserves_mutable_value_identity_for_nested_structures(self):
        nested = {'inner': [1, 2]}
        f = CharField(error_messages={'nest': nested})
        f_copy = copy.deepcopy(f)
        self.assertIs(f_copy.error_messages['nest'], nested)
        nested['inner'].append(3)
        self.assertEqual(f_copy.error_messages['nest']['inner'], [1, 2, 3])