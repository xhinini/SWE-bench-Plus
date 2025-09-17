from django.contrib.admin.options import BaseModelAdmin, ModelAdmin, InlineModelAdmin, StackedInline, TabularInline
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.models import User
from django.test import RequestFactory, SimpleTestCase
from django.contrib.admin.options import BaseModelAdmin, ModelAdmin, InlineModelAdmin, StackedInline, TabularInline

class GetInlinesHookTests(SimpleTestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.site = AdminSite()

    def test_base_model_admin_has_get_inlines_and_returns_inlines(self):
        """
        BaseModelAdmin should expose get_inlines(request, obj) and return
        the instance's inlines attribute.
        """
        bm = BaseModelAdmin()
        bm.inlines = ['A', 'B']
        self.assertEqual(bm.get_inlines(self.request, None), ['A', 'B'])
        sentinel = object()
        self.assertEqual(bm.get_inlines(self.request, sentinel), ['A', 'B'])

    def test_inline_model_admin_has_get_inlines_and_returns_inlines(self):
        """
        InlineModelAdmin instances should inherit get_inlines from BaseModelAdmin.
        """

        class MyInline(InlineModelAdmin):
            model = User
        inline = MyInline(User, self.site)
        inline.inlines = ['X']
        self.assertEqual(inline.get_inlines(self.request, None), ['X'])
        self.assertEqual(inline.get_inlines(self.request, 123), ['X'])

    def test_stackedinline_has_get_inlines_and_returns_inlines(self):
        """
        StackedInline (subclass of InlineModelAdmin) should have get_inlines.
        """

        class MyStacked(StackedInline):
            model = User
        stacked = MyStacked(User, self.site)
        stacked.inlines = ['S']
        self.assertEqual(stacked.get_inlines(self.request, None), ['S'])

    def test_tabularinline_has_get_inlines_and_returns_inlines(self):
        """
        TabularInline (subclass of InlineModelAdmin) should have get_inlines.
        """

        class MyTabular(TabularInline):
            model = User
        tab = MyTabular(User, self.site)
        tab.inlines = ['T']
        self.assertEqual(tab.get_inlines(self.request, 'obj'), ['T'])

    def test_generic_tabular_inline_has_get_inlines_and_returns_inlines(self):
        """
        GenericTabularInline (from contenttypes.admin) should also have get_inlines.
        """

        class MyGeneric(GenericTabularInline):
            model = User
        gen = MyGeneric(User, self.site)
        gen.inlines = ['G']
        self.assertEqual(gen.get_inlines(self.request, None), ['G'])

    def test_get_inlines_accepts_obj_argument_on_base(self):
        """
        Ensure the hook accepts an obj argument on BaseModelAdmin-derived classes.
        """
        bm = BaseModelAdmin()
        bm.inlines = ['Z']

        class DummyObj:
            pass
        o = DummyObj()
        self.assertEqual(bm.get_inlines(self.request, o), ['Z'])

    def test_get_inlines_accepts_obj_argument_on_inline(self):
        """
        Ensure the hook accepts an obj argument on InlineModelAdmin-derived classes.
        """

        class MyInline2(InlineModelAdmin):
            model = User
        inline = MyInline2(User, self.site)
        inline.inlines = ['I2']

        class Dummy:
            pass
        self.assertEqual(inline.get_inlines(self.request, Dummy()), ['I2'])

from django.contrib import admin
from django.test import SimpleTestCase
from django.contrib.contenttypes.admin import GenericTabularInline
from .admin import MediaInline, site as admin_site
from .models import Episode, Media
from .tests import MockRequest, MockSuperUser, request as global_request

class GetInlinesRegressionTest(SimpleTestCase):

    def setUp(self):
        self.request = global_request
        self.request.user = MockSuperUser()