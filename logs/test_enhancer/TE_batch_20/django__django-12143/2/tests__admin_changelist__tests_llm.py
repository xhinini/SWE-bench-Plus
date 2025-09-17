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