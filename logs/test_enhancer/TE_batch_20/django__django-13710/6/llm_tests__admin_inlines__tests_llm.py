from django.contrib.admin import TabularInline
from django.test import TestCase, override_settings
from .admin import site as admin_site
from .models import ProfileCollection, Person
from django.contrib.admin import TabularInline
from django.test import TestCase, override_settings
from .admin import site as admin_site
from .models import ProfileCollection, Person

@override_settings(ROOT_URLCONF='admin_inlines.urls')
class TestInlineVerboseNamePluralDerived(TestCase):
    """
    Regression tests for InlineModelAdmin.verbose_name_plural derivation.
    These tests assert that when an inline explicitly sets verbose_name
    (even if equal to the model's verbose_name) and doesn't set
    verbose_name_plural, the InlineModelAdmin derives verbose_name_plural
    from the explicit verbose_name by appending "s".
    """

    def test_derived_plural_case_1(self):
        Proxy = self._make_proxy(Person, 'PersonSpecialCase1', 'PeopleSpecial1')
        self._assert_plural_derived(Proxy)

    def test_derived_plural_case_2(self):
        Proxy = self._make_proxy(Person, 'Mouse', 'Mice')
        self._assert_plural_derived(Proxy)

    def test_derived_plural_case_3(self):
        Proxy = self._make_proxy(Person, 'Child', 'Children')
        self._assert_plural_derived(Proxy)

    def test_derived_plural_case_4(self):
        Proxy = self._make_proxy(Person, 'Index', 'Indices')
        self._assert_plural_derived(Proxy)

    def test_derived_plural_case_5(self):
        Proxy = self._make_proxy(Person, 'Status', 'Statuses')
        self._assert_plural_derived(Proxy)

    def test_derived_plural_case_6(self):
        Proxy = self._make_proxy(Person, 'Analysis', 'Analyses')
        self._assert_plural_derived(Proxy)

    def test_derived_plural_case_7(self):
        Proxy = self._make_proxy(Person, 'Cactus', 'Cacti')
        self._assert_plural_derived(Proxy)

    def test_derived_plural_case_8(self):
        Proxy = self._make_proxy(Person, 'PersonSpecialCase8', 'Peeps8')
        self._assert_plural_derived(Proxy)

    def test_derived_plural_case_9(self):
        Proxy = self._make_proxy(Person, 'Datum', 'Data')
        self._assert_plural_derived(Proxy)

    def test_derived_plural_case_10(self):
        Proxy = self._make_proxy(Person, 'SpeciesThing', 'Species')
        self._assert_plural_derived(Proxy)