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

from django.utils.translation import gettext_lazy as _lazy
from django.utils.functional import Promise
from django.utils.text import format_lazy
from django.test import TestCase, override_settings
from django.utils.translation import gettext_lazy as _lazy
from django.utils.functional import Promise
from django.utils.text import format_lazy
from django.contrib.admin import TabularInline, StackedInline
from .admin import site as admin_site
from .models import Profile, ProfileCollection, VerboseNameProfile, VerboseNamePluralProfile
from django.contrib.admin.options import InlineModelAdmin

@override_settings(ROOT_URLCONF='admin_inlines.urls')
class InlineVerboseNamePluralLazyTests(TestCase):
    """
    Regression tests for verbose_name / verbose_name_plural handling in
    InlineModelAdmin subclasses. The gold patch preserves laziness by using
    format_lazy('{}s', verbose_name) instead of str(verbose_name) + 's'.
    The candidate patch coerces to str which yields plain str instead of a
    lazy Promise. These tests would fail under the candidate patch.
    """

    def test_tabularinline_lazy_verbose_name_produces_lazy_plural(self):

        class LazyTabular(TabularInline):
            model = Profile
            verbose_name = _lazy('Lazy profile')
        inline = LazyTabular(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)

    def test_stackedinline_lazy_verbose_name_produces_lazy_plural(self):

        class LazyStacked(StackedInline):
            model = Profile
            verbose_name = _lazy('Stacked profile')
        inline = LazyStacked(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)

    def test_inlinemodeladmin_lazy_verbose_name_produces_lazy_plural(self):

        class LazyInlineDirect(InlineModelAdmin):
            model = Profile
            verbose_name = _lazy('Direct inline profile')
        inline = LazyInlineDirect(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)

    def test_lazy_plural_for_different_model_tabular(self):

        class LazyTabularOther(TabularInline):
            model = VerboseNameProfile
            verbose_name = _lazy('Other lazy')
        inline = LazyTabularOther(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), str(format_lazy('{}s', inline.verbose_name)))

    def test_lazy_plural_for_different_model_stacked(self):

        class LazyStackedOther(StackedInline):
            model = VerboseNameProfile
            verbose_name = _lazy('Other stacked lazy')
        inline = LazyStackedOther(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)

    def test_lazy_verbose_name_with_unicode_characters(self):

        class UnicodeLazy(TabularInline):
            model = Profile
            verbose_name = _lazy('Ünicode name')
        inline = UnicodeLazy(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), str(format_lazy('{}s', inline.verbose_name)))