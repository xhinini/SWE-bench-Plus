def test_get_edited_object_pks_with_dollar_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form$-TOTAL_FORMS': '2', 'form$-INITIAL_FORMS': '2', 'form$-MIN_NUM_FORMS': '0', 'form$-MAX_NUM_FORMS': '1000', 'form$-0-uuid': str(a.pk), 'form$-1-uuid': str(b.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix='form$')
    self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]))

def test_get_edited_object_pks_with_dot_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form.test-TOTAL_FORMS': '2', 'form.test-INITIAL_FORMS': '2', 'form.test-MIN_NUM_FORMS': '0', 'form.test-MAX_NUM_FORMS': '1000', 'form.test-0-uuid': str(a.pk), 'form.test-1-uuid': str(b.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix='form.test')
    self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]))

def test_get_edited_object_pks_with_bracket_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form[1]-TOTAL_FORMS': '2', 'form[1]-INITIAL_FORMS': '2', 'form[1]-MIN_NUM_FORMS': '0', 'form[1]-MAX_NUM_FORMS': '1000', 'form[1]-0-uuid': str(a.pk), 'form[1]-1-uuid': str(b.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix='form[1]')
    self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]))

def test_get_edited_object_pks_with_plus_and_star_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefixes = ['form+extra', 'form*']
    for prefix in prefixes:
        data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-1-uuid': str(b.pk)}
        request = self.factory.post('/swallow/', data=data)
        pks = m._get_edited_object_pks(request, prefix=prefix)
        self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]), msg='Failed for prefix %r' % prefix)

def test_get_list_editable_queryset_with_regex_prefixes(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefixes = ['form$', 'form.test', 'form[1]', 'form+extra', 'form*', '^form', 'form(1)', 'form?x', 'form|pipe', 'form€']
    for prefix in prefixes:
        data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
        request = self.factory.post('/swallow/', data=data)
        queryset = m._get_list_editable_queryset(request, prefix=prefix)
        self.assertEqual(queryset.count(), 1, msg='Failed filtering for prefix %r' % prefix)

def test_get_list_editable_queryset_with_invalid_pk_and_regex_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form$'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': 'INVALD_PRIMARY_KEY', f'{prefix}-0-load': '10', '_save': 'Save'}
    request = self.factory.post('/swallow/', data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 2)

def test_get_edited_object_pks_with_caret_and_pipe_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    for prefix in ['^form', 'form|pipe']:
        data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-1-uuid': str(b.pk)}
        request = self.factory.post('/swallow/', data=data)
        pks = m._get_edited_object_pks(request, prefix=prefix)
        self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]))

def test_get_edited_object_pks_with_unicode_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form€'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-1-uuid': str(b.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]))

from django.urls import reverse
from .models import Swallow
from .admin import SwallowAdmin, site as custom_site
from .tests import ChangeListTests as BaseChangeListTests

def _make_changelist_url():
    return reverse('admin:admin_changelist_swallow_changelist')

def _attach_test_method(name, prefix):

    def test_method(self):
        a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
        Swallow.objects.create(origin='Swallow B', load=2, speed=2)
        changelist_url = _make_changelist_url()
        data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
        superuser = self._create_superuser('superuser_test_' + name)
        self.client.force_login(superuser)
        m = SwallowAdmin(Swallow, custom_site)
        request = self.factory.post(changelist_url, data=data)
        pks = m._get_edited_object_pks(request, prefix=prefix)
        self.assertEqual(sorted(pks), sorted([str(a.pk)]))
        qs = m._get_list_editable_queryset(request, prefix=prefix)
        self.assertEqual(qs.count(), 1)
    test_method.__name__ = name
    setattr(BaseChangeListTests, name, test_method)
prefixes = ['form[1]', 'form.test', 'form+extra', 'form*', 'form?', 'form^pref', 'form|pipe', 'form{2}', 'form(abc)', 'form$']
for i, pref in enumerate(prefixes, start=1):
    _attach_test_method(f'test_get_list_editable_queryset_with_regex_prefix_{i}', pref)

def _make_post_data_for_prefix(prefix, a_pk):
    """
    Helper that constructs POST data similar to what the changelist view
    produces for list_editable with the given prefix.
    """
    return {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a_pk), f'{prefix}-0-load': '10', '_save': 'Save'}

def test_get_edited_object_ids_with_prefix_dot(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form.'
    data = _make_post_data_for_prefix(prefix, a.pk)
    request = self.factory.post(reverse('admin:admin_changelist_swallow_changelist'), data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(sorted(pks), sorted([str(a.pk)]))

def test_get_list_editable_queryset_with_prefix_dot(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form.'
    data = _make_post_data_for_prefix(prefix, a.pk)
    request = self.factory.post(reverse('admin:admin_changelist_swallow_changelist'), data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_edited_object_ids_with_prefix_dollar(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form$'
    data = _make_post_data_for_prefix(prefix, a.pk)
    request = self.factory.post(reverse('admin:admin_changelist_swallow_changelist'), data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(sorted(pks), sorted([str(a.pk)]))

def test_get_list_editable_queryset_with_prefix_dollar(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form$'
    data = _make_post_data_for_prefix(prefix, a.pk)
    request = self.factory.post(reverse('admin:admin_changelist_swallow_changelist'), data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_edited_object_ids_with_prefix_caret(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form^'
    data = _make_post_data_for_prefix(prefix, a.pk)
    request = self.factory.post(reverse('admin:admin_changelist_swallow_changelist'), data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(sorted(pks), sorted([str(a.pk)]))

def test_get_list_editable_queryset_with_prefix_caret(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form^'
    data = _make_post_data_for_prefix(prefix, a.pk)
    request = self.factory.post(reverse('admin:admin_changelist_swallow_changelist'), data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_edited_object_ids_with_prefix_asterisk(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form*'
    data = _make_post_data_for_prefix(prefix, a.pk)
    request = self.factory.post(reverse('admin:admin_changelist_swallow_changelist'), data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(sorted(pks), sorted([str(a.pk)]))

def test_get_list_editable_queryset_with_prefix_asterisk(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form*'
    data = _make_post_data_for_prefix(prefix, a.pk)
    request = self.factory.post(reverse('admin:admin_changelist_swallow_changelist'), data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_edited_object_ids_with_prefix_bracket(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form['
    data = _make_post_data_for_prefix(prefix, a.pk)
    request = self.factory.post(reverse('admin:admin_changelist_swallow_changelist'), data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(sorted(pks), sorted([str(a.pk)]))

def test_get_list_editable_queryset_with_prefix_bracket(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form['
    data = _make_post_data_for_prefix(prefix, a.pk)
    request = self.factory.post(reverse('admin:admin_changelist_swallow_changelist'), data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_edited_object_ids_with_dot_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form.test-0-uuid': str(a.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix='form.test')
    self.assertEqual(pks, [str(a.pk)])

def test_get_edited_object_ids_with_plus_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form+extra-0-uuid': str(a.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix='form+extra')
    self.assertEqual(pks, [str(a.pk)])

def test_get_edited_object_ids_with_star_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form*prefix-0-uuid': str(a.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix='form*prefix')
    self.assertEqual(pks, [str(a.pk)])

def test_get_edited_object_ids_with_brackets_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form[1]-0-uuid': str(a.pk), 'form[1]-1-uuid': str(b.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix='form[1]')
    self.assertCountEqual(pks, [str(a.pk), str(b.pk)])

def test_get_edited_object_ids_with_caret_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'weird^prefix-0-uuid': str(a.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix='weird^prefix')
    self.assertEqual(pks, [str(a.pk)])

def test_get_edited_object_ids_with_parentheses_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'paren(prefix)-0-uuid': str(a.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix='paren(prefix)')
    self.assertEqual(pks, [str(a.pk)])

def test_get_edited_object_ids_with_pipe_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'bar|baz-0-uuid': str(a.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix='bar|baz')
    self.assertEqual(pks, [str(a.pk)])

def test_get_edited_object_ids_with_multiple_digits_index(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form.test-12-uuid': str(a.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix='form.test')
    self.assertEqual(pks, [str(a.pk)])

def test_get_edited_object_ids_ignores_nonmatching_keys(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form.test-0-uuid-extra': str(a.pk), 'form.test-0-uuid': str(a.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks = m._get_edited_object_pks(request, prefix='form.test')
    self.assertEqual(pks, [str(a.pk)])

def test_get_edited_object_ids_multiple_prefixes(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form$-0-uuid': str(a.pk), 'other[1]-0-uuid': str(b.pk)}
    request = self.factory.post('/swallow/', data=data)
    pks_form_dollar = m._get_edited_object_pks(request, prefix='form$')
    pks_other_bracket = m._get_edited_object_pks(request, prefix='other[1]')
    self.assertEqual(pks_form_dollar, [str(a.pk)])
    self.assertEqual(pks_other_bracket, [str(b.pk)])

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from .admin import SwallowAdmin, site as custom_site
from .models import Swallow

class RegexPrefixListEditableTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

def test_get_edited_object_pks_with_dot_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser')
    m = SwallowAdmin(Swallow, custom_site)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form.test-TOTAL_FORMS': '2', 'form.test-INITIAL_FORMS': '2', 'form.test-MIN_NUM_FORMS': '0', 'form.test-MAX_NUM_FORMS': '1000', 'form.test-0-uuid': str(a.pk), 'form.test-1-uuid': str(b.pk)}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix='form.test')
    self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]))

def test_get_edited_object_pks_with_bracket_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    data = {'form[1]-TOTAL_FORMS': '2', 'form[1]-INITIAL_FORMS': '2', 'form[1]-MIN_NUM_FORMS': '0', 'form[1]-MAX_NUM_FORMS': '1000', 'form[1]-0-uuid': str(a.pk), 'form[1]-1-uuid': str(b.pk)}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix='form[1]')
    self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]))

def test_get_edited_object_pks_with_plus_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    prefix = 'form+extra'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-1-uuid': str(b.pk)}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]))

def test_get_edited_object_pks_with_star_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    prefix = 'form*'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-1-uuid': str(b.pk)}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]))

def test_get_edited_object_pks_with_parentheses_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    prefix = 'form(1)'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-1-uuid': str(b.pk)}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]))

def test_get_edited_object_pks_with_pipe_and_caret_prefixes(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    for prefix in ('form|1', 'form^'):
        data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-1-uuid': str(b.pk)}
        request = self.factory.post(changelist_url, data=data)
        pks = m._get_edited_object_pks(request, prefix=prefix)
        self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]))

def test_get_edited_object_pks_with_backslash_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    prefix = 'form\\\\x'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-1-uuid': str(b.pk)}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk)]))

def test_get_list_editable_queryset_with_various_regex_like_prefixes(self):
    prefixes = ['form.test', 'form[1]', 'form+extra', 'form*', 'form(1)']
    for prefix in prefixes:
        a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
        Swallow.objects.create(origin='Swallow B', load=2, speed=2)
        m = SwallowAdmin(Swallow, custom_site)
        changelist_url = reverse('admin:admin_changelist_swallow_changelist')
        data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
        request = self.factory.post(changelist_url, data=data)
        queryset = m._get_list_editable_queryset(request, prefix=prefix)
        self.assertEqual(queryset.count(), 1, msg='Failed for prefix: %s' % prefix)

def test_get_list_editable_queryset_with_invalid_pk_returns_unfiltered(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    m = SwallowAdmin(Swallow, custom_site)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    prefix = 'form.test'
    data = {f'{prefix}-TOTAL_FORMS': '1', f'{prefix}-INITIAL_FORMS': '1', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': 'INVALID_PKEY', f'{prefix}-0-load': '10', '_save': 'Save'}
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 2)

from django.test import TestCase, override_settings
from django.test.client import RequestFactory
from django.urls import reverse
from .admin import SwallowAdmin, site as custom_site
from .models import Swallow

@override_settings(ROOT_URLCONF='admin_changelist.urls')
class RegexPrefixListEditableTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def _create_swallow_objects(self):
        a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
        b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
        c = Swallow.objects.create(origin='Swallow C', load=5, speed=5)
        return (a, b, c)

    def _admin_instance(self):
        return SwallowAdmin(Swallow, custom_site)

def test_get_edited_object_pks_with_dot_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser_dot')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form.part'
    data = {f'{prefix}-TOTAL_FORMS': '1', f'{prefix}-INITIAL_FORMS': '1', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(sorted(pks), [str(a.pk)])

def test_get_edited_object_pks_with_brackets_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form[1]'
    data = {f'{prefix}-TOTAL_FORMS': '1', f'{prefix}-INITIAL_FORMS': '1', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), '_save': 'Save'}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(pks, [str(a.pk)])

def test_get_edited_object_pks_with_parentheses_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form(1)'
    data = {f'{prefix}-TOTAL_FORMS': '1', f'{prefix}-INITIAL_FORMS': '1', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), '_save': 'Save'}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(pks, [str(a.pk)])

def test_get_edited_object_pks_with_plus_and_star_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    for prefix in ('form+extra', 'form*star'):
        data = {f'{prefix}-TOTAL_FORMS': '1', f'{prefix}-INITIAL_FORMS': '1', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), '_save': 'Save'}
        request = self.factory.post(changelist_url, data=data)
        pks = m._get_edited_object_pks(request, prefix=prefix)
        self.assertEqual(pks, [str(a.pk)], msg='Failed for prefix %r' % prefix)

def test_get_edited_object_pks_with_question_and_caret_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    for prefix in ('form?maybe', '^form'):
        data = {f'{prefix}-TOTAL_FORMS': '1', f'{prefix}-INITIAL_FORMS': '1', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), '_save': 'Save'}
        request = self.factory.post(changelist_url, data=data)
        pks = m._get_edited_object_pks(request, prefix=prefix)
        self.assertEqual(pks, [str(a.pk)], msg='Failed for prefix %r' % prefix)

def test_get_edited_object_pks_with_curly_and_backslash_in_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form{1}'
    data = {f'{prefix}-TOTAL_FORMS': '1', f'{prefix}-INITIAL_FORMS': '1', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), '_save': 'Save'}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(pks, [str(a.pk)])
    prefix = 'form\\back'
    data = {f'{prefix}-TOTAL_FORMS': '1', f'{prefix}-INITIAL_FORMS': '1', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), '_save': 'Save'}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(pks, [str(a.pk)])

def test_get_list_editable_queryset_with_many_regex_like_prefixes(self):
    """
    Ensure _get_list_editable_queryset accepts a variety of prefixes with
    regex-like characters and still returns a filtered queryset.
    """
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    prefixes = ['form$', 'form.part', 'form[1]', 'form(1)', 'form+1', 'form*1', 'form?1', '^form', 'form{1}', 'form\\x']
    for prefix in prefixes:
        data = {f'{prefix}-TOTAL_FORMS': '1', f'{prefix}-INITIAL_FORMS': '1', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), '_save': 'Save'}
        request = self.factory.post(changelist_url, data=data)
        qs = m._get_list_editable_queryset(request, prefix=prefix)
        self.assertEqual(qs.count(), 1, msg='Failed for prefix %r' % prefix)

def test_get_list_editable_queryset_with_brackets_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    prefix = 'form[1]'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
    superuser = self._create_superuser('superuser_brackets')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_list_editable_queryset_with_dot_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    prefix = 'form.test'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
    superuser = self._create_superuser('superuser_dot')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_list_editable_queryset_with_plus_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    prefix = 'form+extra'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
    superuser = self._create_superuser('superuser_plus')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_list_editable_queryset_with_star_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    prefix = 'form*'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
    superuser = self._create_superuser('superuser_star')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_list_editable_queryset_with_paren_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    prefix = 'form(1)'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
    superuser = self._create_superuser('superuser_paren')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_list_editable_queryset_with_pipe_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    prefix = 'form|pipe'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
    superuser = self._create_superuser('superuser_pipe')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_list_editable_queryset_with_caret_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    prefix = 'form^'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
    superuser = self._create_superuser('superuser_caret')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_list_editable_queryset_with_question_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    prefix = 'form?'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
    superuser = self._create_superuser('superuser_question')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_edited_object_pks_with_brackets_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    c = Swallow.objects.create(origin='Swallow C', load=5, speed=5)
    prefix = 'form[1]'
    superuser = self._create_superuser('superuser_pks')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    data = {f'{prefix}-TOTAL_FORMS': '3', f'{prefix}-INITIAL_FORMS': '3', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-1-uuid': str(b.pk), f'{prefix}-2-uuid': str(c.pk), f'{prefix}-0-load': '9.0', f'{prefix}-1-load': '5.0', f'{prefix}-2-load': '5.0', '_save': 'Save'}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertEqual(sorted(pks), sorted([str(a.pk), str(b.pk), str(c.pk)]))

def test_get_edited_object_pks_with_bracket_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser_bracket')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form[1]-TOTAL_FORMS': '2', 'form[1]-INITIAL_FORMS': '2', 'form[1]-MIN_NUM_FORMS': '0', 'form[1]-MAX_NUM_FORMS': '1000', 'form[1]-0-uuid': str(a.pk), 'form[1]-1-uuid': str(b.pk)}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix='form[1]')
    self.assertCountEqual(pks, [str(a.pk), str(b.pk)])

def test_get_list_editable_queryset_with_dot_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser_dot')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form.test-TOTAL_FORMS': '2', 'form.test-INITIAL_FORMS': '2', 'form.test-MIN_NUM_FORMS': '0', 'form.test-MAX_NUM_FORMS': '1000', 'form.test-0-uuid': str(a.pk), 'form.test-0-load': '10', '_save': 'Save'}
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix='form.test')
    self.assertEqual(queryset.count(), 1)

def test_get_edited_object_pks_with_plus_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    superuser = self._create_superuser('superuser_plus')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form+extra-TOTAL_FORMS': '1', 'form+extra-INITIAL_FORMS': '1', 'form+extra-MIN_NUM_FORMS': '0', 'form+extra-MAX_NUM_FORMS': '1000', 'form+extra-0-uuid': str(a.pk)}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix='form+extra')
    self.assertEqual(pks, [str(a.pk)])

def test_get_list_editable_queryset_with_star_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser_star')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form*-TOTAL_FORMS': '2', 'form*-INITIAL_FORMS': '2', 'form*-MIN_NUM_FORMS': '0', 'form*-MAX_NUM_FORMS': '1000', 'form*-0-uuid': str(a.pk), 'form*-0-load': '10', '_save': 'Save'}
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix='form*')
    self.assertEqual(queryset.count(), 1)

def test_get_edited_object_pks_with_paren_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser_paren')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form(1)-TOTAL_FORMS': '2', 'form(1)-INITIAL_FORMS': '2', 'form(1)-MIN_NUM_FORMS': '0', 'form(1)-MAX_NUM_FORMS': '1000', 'form(1)-0-uuid': str(a.pk), 'form(1)-1-uuid': str(b.pk)}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix='form(1)')
    self.assertCountEqual(pks, [str(a.pk), str(b.pk)])

def test_get_list_editable_queryset_with_backslash_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser_backslash')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'form\\'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-0-load': '10', '_save': 'Save'}
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix=prefix)
    self.assertEqual(queryset.count(), 1)

def test_get_edited_object_pks_with_brace_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    superuser = self._create_superuser('superuser_brace')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form{X}-TOTAL_FORMS': '1', 'form{X}-INITIAL_FORMS': '1', 'form{X}-MIN_NUM_FORMS': '0', 'form{X}-MAX_NUM_FORMS': '1000', 'form{X}-0-uuid': str(a.pk)}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix='form{X}')
    self.assertEqual(pks, [str(a.pk)])

def test_get_list_editable_queryset_with_question_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser_question')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    data = {'form?-TOTAL_FORMS': '2', 'form?-INITIAL_FORMS': '2', 'form?-MIN_NUM_FORMS': '0', 'form?-MAX_NUM_FORMS': '1000', 'form?-0-uuid': str(a.pk), 'form?-0-load': '10', '_save': 'Save'}
    request = self.factory.post(changelist_url, data=data)
    queryset = m._get_list_editable_queryset(request, prefix='form?')
    self.assertEqual(queryset.count(), 1)

def test_get_edited_object_pks_with_mixed_regex_chars_prefix(self):
    a = Swallow.objects.create(origin='Swallow A', load=4, speed=1)
    b = Swallow.objects.create(origin='Swallow B', load=2, speed=2)
    superuser = self._create_superuser('superuser_mixed')
    self.client.force_login(superuser)
    changelist_url = reverse('admin:admin_changelist_swallow_changelist')
    m = SwallowAdmin(Swallow, custom_site)
    prefix = 'f.or+(1)[x]$'
    data = {f'{prefix}-TOTAL_FORMS': '2', f'{prefix}-INITIAL_FORMS': '2', f'{prefix}-MIN_NUM_FORMS': '0', f'{prefix}-MAX_NUM_FORMS': '1000', f'{prefix}-0-uuid': str(a.pk), f'{prefix}-1-uuid': str(b.pk)}
    request = self.factory.post(changelist_url, data=data)
    pks = m._get_edited_object_pks(request, prefix=prefix)
    self.assertCountEqual(pks, [str(a.pk), str(b.pk)])