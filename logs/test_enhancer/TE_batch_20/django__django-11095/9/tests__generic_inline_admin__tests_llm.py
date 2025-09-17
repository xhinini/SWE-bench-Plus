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

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth.models import User
from generic_inline_admin.models import Episode
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth.models import User
from generic_inline_admin.models import Episode
from django.http import HttpRequest

@override_settings(ROOT_URLCONF='generic_inline_admin.urls')
class DynamicInlinesRegressionTests(TestCase):

    def _make_request(self, path='/', user=None):
        req = self.factory.get(path)
        req.user = user or self.superuser
        return req

from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin, ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import SimpleTestCase, RequestFactory

class GetInlinesRegressionTests(SimpleTestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')

    def test_base_model_admin_get_inlines_returns_inlines_attribute(self):

        class MyBaseAdmin(BaseModelAdmin):
            inlines = ['INLINE_A']
        admin_inst = MyBaseAdmin()
        self.assertEqual(admin_inst.get_inlines(self.request, None), ['INLINE_A'])

    def test_base_model_admin_get_inlines_requires_obj_argument(self):

        class MyBaseAdmin(BaseModelAdmin):
            inlines = ['INLINE_A']
        admin_inst = MyBaseAdmin()
        with self.assertRaises(TypeError):
            admin_inst.get_inlines(self.request)

    def test_inline_model_admin_inherits_get_inlines(self):

        class MyInline(InlineModelAdmin):
            model = User
            inlines = ['INLINE_B']
        inline_inst = MyInline(User, AdminSite())
        self.assertEqual(inline_inst.get_inlines(self.request, None), ['INLINE_B'])

    def test_inline_model_admin_get_inlines_requires_obj_argument(self):

        class MyInline(InlineModelAdmin):
            model = User
            inlines = ['INLINE_B']
        inline_inst = MyInline(User, AdminSite())
        with self.assertRaises(TypeError):
            inline_inst.get_inlines(self.request)

    def test_modeladmin_get_inlines_requires_obj_when_inherited_from_base(self):

        class MyInline(InlineModelAdmin):
            model = User

        class MyModelAdmin(ModelAdmin):
            inlines = [MyInline]
        ma = MyModelAdmin(User, AdminSite())
        with self.assertRaises(TypeError):
            ma.get_inlines(self.request)

    def test_get_inlines_on_inline_instance_does_not_depend_on_modeladmin_only(self):

        class MyInline(InlineModelAdmin):
            model = User
            inlines = ['I']
        inline_inst = MyInline(User, AdminSite())
        self.assertEqual(inline_inst.get_inlines(self.request, None), ['I'])

from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin, ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import SimpleTestCase
from unittest.mock import patch
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin, ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import SimpleTestCase
from unittest.mock import patch

class GetInlinesRegressionTests(SimpleTestCase):

    def setUp(self):
        self.site = AdminSite()

    def test_modeladmin_get_inline_instances_honours_empty_list_from_base_get_inlines(self):
        ma = ModelAdmin(User, self.site)
        request = object()
        with patch.object(BaseModelAdmin, 'get_inlines', return_value=[]):
            instances = ma.get_inline_instances(request, obj=None)
        self.assertEqual(instances, [])

from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.test import SimpleTestCase
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.test import SimpleTestCase
from .models import Episode, Media

class GetInlinesRegressionTests(SimpleTestCase):

    def setUp(self):
        self.site = AdminSite()

from types import SimpleNamespace
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin, ModelAdmin
from types import SimpleNamespace
from django.test import SimpleTestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin, ModelAdmin

class GetInlinesRegressionTests(SimpleTestCase):

    def setUp(self):
        self.admin_site = AdminSite()
        self.request = object()

        class Req:
            pass
        self.truthy_request = Req()
        self.truthy_request.user = None

    def test_get_inlines_not_shadowed_by_modeladmin_method(self):
        """
        Ensure BaseModelAdmin.get_inlines is the hook used if not overridden,
        and returns the inlines attribute even when ModelAdmin also defines inlines.
        """

        class MyInline(InlineModelAdmin):
            model = DummyModel
        inline = MyInline(DummyParentModel, self.admin_site)
        inline.inlines = ['i1']
        self.assertEqual(inline.get_inlines(self.request, None), ['i1'])