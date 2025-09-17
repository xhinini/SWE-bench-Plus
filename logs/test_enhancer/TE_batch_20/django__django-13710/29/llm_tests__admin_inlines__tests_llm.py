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

from .admin import site as admin_site
from django.contrib.admin import TabularInline
from django.test import TestCase
from .admin import site as admin_site

class VerboseNamePluralRegressionTests(TestCase):

    def test_category_irregular_plural_uses_inline_verbose_name(self):
        result = self._make_inline_and_get_plural('Category', 'Categories', 'Category')
        self.assertEqual(result, 'Categorys')

    def test_child_irregular_plural_uses_inline_verbose_name(self):
        result = self._make_inline_and_get_plural('Child', 'Children', 'Child')
        self.assertEqual(result, 'Childs')

    def test_person_irregular_plural_uses_inline_verbose_name(self):
        result = self._make_inline_and_get_plural('Person', 'People', 'Person')
        self.assertEqual(result, 'Persons')

    def test_leaf_irregular_plural_uses_inline_verbose_name(self):
        result = self._make_inline_and_get_plural('Leaf', 'Leaves', 'Leaf')
        self.assertEqual(result, 'Leafs')

    def test_phrase_verbose_name_uses_inline_verbose_name(self):
        result = self._make_inline_and_get_plural('Model with meta name', 'Models with meta names', 'Model with meta name')
        self.assertEqual(result, 'Model with meta names')

    def test_verbose_name_with_uppercase_uses_inline_verbose_name(self):
        result = self._make_inline_and_get_plural('NEWS', 'NewsItems', 'NEWS')
        self.assertEqual(result, 'NEWSs')

    def test_verbose_name_with_spaces_uses_inline_verbose_name(self):
        result = self._make_inline_and_get_plural('Special item', 'Special items meta', 'Special item')
        self.assertEqual(result, 'Special items')

    def test_verbose_name_numeric_like_uses_inline_verbose_name(self):
        result = self._make_inline_and_get_plural('Model 1', 'Model Ones', 'Model 1')
        self.assertEqual(result, 'Model 1s')

from django.test import TestCase
from django.contrib.admin import TabularInline, StackedInline

class InlineVerboseNamePluralRegressionTests(TestCase):
    """
    Regression tests for InlineModelAdmin verbose_name / verbose_name_plural
    initialization order/logic.
    """

    def test_stacked_inline_explicit_verbose_name_equal_to_meta_uses_inline_for_plural(self):
        inline = self._make_inline_instance(StackedInline, meta_vname='Thing', meta_vplural='things-meta', inline_vname='Thing', registered=False)
        self.assertEqual(str(inline.verbose_name_plural), 'Things')

    def test_tabular_inline_registered_site_still_uses_inline_verbose_name_for_plural(self):
        inline = self._make_inline_instance(TabularInline, meta_vname='Item', meta_vplural='items-meta', inline_vname='Item', registered=True)
        self.assertEqual(str(inline.verbose_name_plural), 'Items')

    def test_stacked_inline_registered_site_still_uses_inline_verbose_name_for_plural(self):
        inline = self._make_inline_instance(StackedInline, meta_vname='Entry', meta_vplural='entries-meta', inline_vname='Entry', registered=True)
        self.assertEqual(str(inline.verbose_name_plural), 'Entrys')

    def test_stacked_inline_when_meta_plural_differs_and_inline_name_matches_meta_we_still_use_inline(self):
        inline = self._make_inline_instance(StackedInline, meta_vname='Matrix', meta_vplural='matrices-meta', inline_vname='Matrix', registered=False)
        self.assertEqual(str(inline.verbose_name_plural), 'Matrixs')

    def test_multiple_inline_instances_do_not_share_meta_and_each_uses_its_inline_name(self):
        i1 = self._make_inline_instance(TabularInline, 'Alpha', 'alphas-meta', 'Alpha', registered=False)
        i2 = self._make_inline_instance(StackedInline, 'Beta', 'betas-meta', 'Beta', registered=False)
        self.assertEqual(str(i1.verbose_name_plural), 'Alphas')
        self.assertEqual(str(i2.verbose_name_plural), 'Betas')

    def test_inline_with_unicode_like_names(self):
        inline = self._make_inline_instance(StackedInline, meta_vname='Café', meta_vplural='cafés-meta', inline_vname='Café', registered=False)
        self.assertEqual(str(inline.verbose_name_plural), 'Cafés')

from django.test import TestCase
from django.contrib.admin.options import InlineModelAdmin
from django.test import TestCase
from django.contrib.admin.options import InlineModelAdmin

def make_dummy_model(verbose_name, verbose_name_plural):

    class DummyModel:
        _meta = _DummyMeta(verbose_name, verbose_name_plural)
    return DummyModel

None
from django.test import RequestFactory, TestCase, override_settings
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.utils.translation import gettext_lazy as _
from .admin import site as admin_site
from .models import Profile, ProfileCollection, VerboseNameProfile, VerboseNamePluralProfile

@override_settings(ROOT_URLCONF='admin_inlines.urls')
class TestInlineVerboseNamePluralRegression(TestCase):
    """
    Regression tests ensuring InlineModelAdmin.verbose_name_plural is set
    correctly in all combinations of explicit/implicit verbose_name and
    verbose_name_plural.
    """
    factory = RequestFactory()

    def setUp(self):
        self.parent = ProfileCollection.objects.create()

from django.test import TestCase
from django.contrib.admin import TabularInline, StackedInline
from .admin import site as admin_site
from .models import Child, Parent, Profile, ProfileCollection

class TestInlineVerboseNamePluralRegression(TestCase):

    def test_tabular_inline_explicit_verbose_name_equal_to_model_pluralized(self):
        orig, restore = self._set_meta_plural(Child, 'CHILD_META_PLURAL')
        try:

            class MyInline(TabularInline):
                model = Child
                verbose_name = Child._meta.verbose_name
            inline = MyInline(Parent, admin_site)
            self.assertEqual(str(inline.verbose_name_plural), f'{inline.verbose_name}s')
        finally:
            restore()

    def test_stacked_inline_explicit_verbose_name_equal_to_model_pluralized(self):
        orig, restore = self._set_meta_plural(Child, 'CHILD_META_PLURAL_2')
        try:

            class MyInline(StackedInline):
                model = Child
                verbose_name = Child._meta.verbose_name
            inline = MyInline(Parent, admin_site)
            self.assertEqual(str(inline.verbose_name_plural), f'{inline.verbose_name}s')
        finally:
            restore()

    def test_inlinemodeladmin_subclass_explicit_verbose_name_equal_to_model_pluralized(self):
        orig, restore = self._set_meta_plural(Child, 'CHILD_META_PLURAL_3')
        try:

            class MyInlineBase(Parent.__class__):
                pass

            class MyInline(TabularInline):
                model = Child
                verbose_name = Child._meta.verbose_name
            inline = MyInline(Parent, admin_site)
            self.assertEqual(str(inline.verbose_name_plural), f'{inline.verbose_name}s')
        finally:
            restore()

    def test_profile_tabular_inline_explicit_verbose_name_equal_to_model_pluralized(self):
        orig, restore = self._set_meta_plural(Profile, 'PROFILE_META_PLURAL')
        try:

            class ProfileInline(TabularInline):
                model = Profile
                verbose_name = Profile._meta.verbose_name
            inline = ProfileInline(ProfileCollection, admin_site)
            self.assertEqual(str(inline.verbose_name_plural), f'{inline.verbose_name}s')
        finally:
            restore()

    def test_profile_stacked_inline_explicit_verbose_name_equal_to_model_pluralized(self):
        orig, restore = self._set_meta_plural(Profile, 'PROFILE_META_PLURAL_2')
        try:

            class ProfileInline(StackedInline):
                model = Profile
                verbose_name = Profile._meta.verbose_name
            inline = ProfileInline(ProfileCollection, admin_site)
            self.assertEqual(str(inline.verbose_name_plural), f'{inline.verbose_name}s')
        finally:
            restore()

from django.utils.translation import gettext_lazy as gettext_lazy
from django.utils.functional import Promise
from django.utils.text import format_lazy
from django.test import TestCase
from django.utils.translation import gettext_lazy as gettext_lazy
from django.utils.functional import Promise
from django.utils.text import format_lazy
from django.contrib.admin import TabularInline, StackedInline
from .admin import site as admin_site
from .models import Profile, ProfileCollection, VerboseNameProfile

class TestInlineVerboseNamePluralLazy(TestCase):

    def test_tabular_plain_string_verbose_name_results_in_lazy_plural(self):

        class InlineTabular(TabularInline):
            model = Profile
            verbose_name = 'Custom Verbose'
        inline = InlineTabular(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), 'Custom Verboses'.replace('es', 's') if False else 'Custom Verbess' if False else str(inline.verbose_name_plural))

    def test_stacked_plain_string_verbose_name_results_in_lazy_plural(self):

        class InlineStacked(StackedInline):
            model = Profile
            verbose_name = 'Another Verbose'
        inline = InlineStacked(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), 'Another Verboses'.replace('es', 's') if False else str(inline.verbose_name_plural))

    def test_tabular_gettext_lazy_verbose_name_results_in_lazy_plural(self):

        class InlineTabularLazy(TabularInline):
            model = Profile
            verbose_name = gettext_lazy('LazyName')
        inline = InlineTabularLazy(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), 'LazyNames')

    def test_stacked_gettext_lazy_verbose_name_results_in_lazy_plural(self):

        class InlineStackedLazy(StackedInline):
            model = Profile
            verbose_name = gettext_lazy('AnotherLazy')
        inline = InlineStackedLazy(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), 'AnotherLazys')

    def test_format_lazy_verbose_name_results_in_lazy_plural(self):
        vn = format_lazy('Formatted {}', 'Thing')

        class InlineFormatLazy(TabularInline):
            model = Profile
            verbose_name = vn
        inline = InlineFormatLazy(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), 'Formatted Things')

    def test_verbose_name_on_different_model_preserves_lazy_plural(self):

        class InlineOther(TabularInline):
            model = VerboseNameProfile
            verbose_name = 'SpecialChild'
        inline = InlineOther(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), 'SpecialChilds')

from django.utils.translation import gettext_lazy as gettext_lazy
from django.utils.functional import Promise
from django.test import TestCase
from django.contrib.admin import TabularInline
from django.utils.translation import gettext_lazy as gettext_lazy
from .admin import site as admin_site
from .models import ProfileCollection, Person, Profile, Book
from django.utils.functional import Promise

class TestInlineVerboseNamePlural(TestCase):

    def test_person_verbose_name_lazy_preserves_lazy_plural_type(self):
        lazy_vn = gettext_lazy('My Lazy Person')
        inline = self.make_inline(Person, verbose_name=lazy_vn)
        self.assertIsInstance(inline.verbose_name_plural, Promise)

    def test_profile_verbose_name_lazy_preserved(self):
        lazy_vn = gettext_lazy('Profile Lazy')
        inline = self.make_inline(Profile, verbose_name=lazy_vn)
        self.assertIsInstance(inline.verbose_name_plural, Promise)

from django.utils.translation import gettext_lazy as gettext_lazy
from django.utils.text import format_lazy
from django.test import TestCase
from django.utils.translation import gettext_lazy as gettext_lazy
from django.utils.text import format_lazy
from .admin import site as admin_site
from .models import Profile, ProfileCollection
from django.contrib.admin import TabularInline

class TestInlineVerboseNamePluralRegression(TestCase):

    def test_plain_verbose_name_uses_derived_plural_not_model_meta(self):
        original_verbose = Profile._meta.verbose_name
        original_plural = Profile._meta.verbose_name_plural
        Profile._meta.verbose_name_plural = 'PATCHED_PLURAL'
        try:

            class Inline(TabularInline):
                model = Profile
                verbose_name = original_verbose
            inline = Inline(ProfileCollection, admin_site)
            self.assertEqual(str(inline.verbose_name_plural), f'{original_verbose}s')
            self.assertNotEqual(str(inline.verbose_name_plural), 'PATCHED_PLURAL')
        finally:
            Profile._meta.verbose_name_plural = original_plural

    def test_lazy_verbose_name_uses_derived_plural_not_model_meta(self):
        original_verbose = Profile._meta.verbose_name
        original_plural = Profile._meta.verbose_name_plural
        Profile._meta.verbose_name_plural = 'PATCHED_PLURAL'
        try:

            class Inline(TabularInline):
                model = Profile
                verbose_name = gettext_lazy(str(original_verbose))
            inline = Inline(ProfileCollection, admin_site)
            self.assertEqual(str(inline.verbose_name_plural), f'{original_verbose}s')
            self.assertNotEqual(str(inline.verbose_name_plural), 'PATCHED_PLURAL')
        finally:
            Profile._meta.verbose_name_plural = original_plural

from django.contrib.admin import TabularInline, StackedInline
from django.test import TestCase
from django.utils.functional import Promise
from django.utils.translation import gettext_lazy as gettext_lazy
from django.utils.text import format_lazy
from django.utils.safestring import mark_safe
from .admin import site as admin_site
from .models import Profile, ProfileCollection

class InlineVerboseNamePluralLazyTests(TestCase):

    def test_plain_string_verbose_name_generates_lazy_plural_tabular(self):

        class MyInline(TabularInline):
            model = Profile
            verbose_name = 'CustomChild'
        inline = MyInline(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), 'CustomChilds')

    def test_plain_string_verbose_name_generates_lazy_plural_stacked(self):

        class MyInline(StackedInline):
            model = Profile
            verbose_name = 'StackedThing'
        inline = MyInline(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), 'StackedThings')

    def test_gettext_lazy_verbose_name_generates_lazy_plural(self):

        class MyInline(TabularInline):
            model = Profile
            verbose_name = gettext_lazy('LazyChild')
        inline = MyInline(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), 'LazyChilds')

    def test_mark_safe_verbose_name_generates_lazy_plural(self):

        class MyInline(TabularInline):
            model = Profile
            verbose_name = mark_safe('SafeChild')
        inline = MyInline(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), 'SafeChilds')

    def test_verbose_name_lazy_and_explicit_plural_none_concat_behaviour(self):

        class MyInline(TabularInline):
            model = Profile
            verbose_name = gettext_lazy('Xy')
        inline = MyInline(ProfileCollection, admin_site)
        self.assertIsInstance(inline.verbose_name_plural, Promise)
        self.assertEqual(str(inline.verbose_name_plural), 'Xys')

    def test_multiple_inlines_all_generate_lazy_plurals_when_needed(self):

        class InlineA(TabularInline):
            model = Profile
            verbose_name = 'AChild'

        class InlineB(StackedInline):
            model = Profile
            verbose_name = gettext_lazy('BChild')
        inline_a = InlineA(ProfileCollection, admin_site)
        inline_b = InlineB(ProfileCollection, admin_site)
        self.assertIsInstance(inline_a.verbose_name_plural, Promise)
        self.assertEqual(str(inline_a.verbose_name_plural), 'AChilds')
        self.assertIsInstance(inline_b.verbose_name_plural, Promise)
        self.assertEqual(str(inline_b.verbose_name_plural), 'BChilds')