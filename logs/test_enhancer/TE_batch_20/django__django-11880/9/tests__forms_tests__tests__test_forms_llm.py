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