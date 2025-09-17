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

from django.contrib.admin.options import BaseModelAdmin, ModelAdmin, InlineModelAdmin
from django.contrib.admin.sites import AdminSite
from django.test import SimpleTestCase, RequestFactory
from django.contrib.admin.options import BaseModelAdmin, ModelAdmin, InlineModelAdmin
from django.contrib.admin import AdminSite as DjangoAdminSite

class TestGetInlinesRegression(SimpleTestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.request = self.rf.get('/')
if __name__ == '__main__':
    import django
    from django.conf import settings
    if not settings.configured:
        settings.configure(DEBUG=True)
    django.setup()
    import unittest
    unittest.main()

from django.contrib.admin.options import BaseModelAdmin, ModelAdmin, InlineModelAdmin, StackedInline, TabularInline
from django.contrib.admin.sites import AdminSite
from django.test import SimpleTestCase
import inspect

class GetInlinesAPITest(SimpleTestCase):

    def test_base_model_admin_has_get_inlines(self):
        self.assertTrue(hasattr(BaseModelAdmin, 'get_inlines'))
        self.assertTrue(callable(getattr(BaseModelAdmin, 'get_inlines')))

    def test_inline_model_admin_has_get_inlines(self):
        self.assertTrue(hasattr(InlineModelAdmin, 'get_inlines'))
        self.assertTrue(callable(getattr(InlineModelAdmin, 'get_inlines')))

    def test_stackedinline_has_get_inlines(self):
        self.assertTrue(hasattr(StackedInline, 'get_inlines'))
        self.assertTrue(callable(getattr(StackedInline, 'get_inlines')))

    def test_tabularinline_has_get_inlines(self):
        self.assertTrue(hasattr(TabularInline, 'get_inlines'))
        self.assertTrue(callable(getattr(TabularInline, 'get_inlines')))

    def test_get_inlines_is_callable_on_class_and_instance(self):
        self.assertTrue(callable(getattr(BaseModelAdmin, 'get_inlines')))

        class DummyMeta:
            app_label = 'app'
            model_name = 'm'
        DummyModel = type('DummyModel', (), {'_meta': DummyMeta})
        ma = ModelAdmin(DummyModel, AdminSite())
        self.assertTrue(callable(getattr(ma, 'get_inlines')))

    def test_get_inlines_presence_implies_override_point(self):
        self.assertTrue(hasattr(BaseModelAdmin, 'get_inlines'))

import inspect
from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin, StackedInline, TabularInline
from django.contrib.admin.sites import AdminSite
from django.test import SimpleTestCase
import inspect

class GetInlinesRegressionTests(SimpleTestCase):

    def test_base_model_admin_has_get_inlines_attribute(self):
        self.assertTrue(hasattr(BaseModelAdmin, 'get_inlines'))
        self.assertTrue(callable(getattr(BaseModelAdmin, 'get_inlines')))

    def test_base_model_admin_get_inlines_returns_inlines(self):

        class MyBaseAdmin(BaseModelAdmin):
            inlines = ['A']
        admin = MyBaseAdmin()
        self.assertEqual(admin.get_inlines(None, None), ['A'])

    def test_inline_model_admin_has_get_inlines_attribute(self):
        self.assertTrue(hasattr(InlineModelAdmin, 'get_inlines'))
        self.assertTrue(callable(getattr(InlineModelAdmin, 'get_inlines')))

    def test_stackedinline_has_get_inlines_attribute(self):
        self.assertTrue(hasattr(StackedInline, 'get_inlines'))
        self.assertTrue(callable(getattr(StackedInline, 'get_inlines')))

    def test_tabularinline_has_get_inlines_attribute(self):
        self.assertTrue(hasattr(TabularInline, 'get_inlines'))
        self.assertTrue(callable(getattr(TabularInline, 'get_inlines')))

from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin, ModelAdmin
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.test import SimpleTestCase
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Media, Episode
from .admin import site as admin_site
try:
    from .tests import request as module_request
    REQUEST = module_request
except Exception:
    REQUEST = _Req()

    class _User:

        def has_perm(self, perm):
            return True
    REQUEST.user = _User()

class GetInlinesRegressionTests(SimpleTestCase):
    """Regression tests ensuring get_inlines exists on BaseModelAdmin/InlineModelAdmin
    and that ModelAdmin.get_inline_instances uses get_inlines."""

    def test_tabularinline_has_get_inlines(self):

        class MyInline(admin.TabularInline):
            model = Media
            inlines = ('a',)
        inline = MyInline(Episode, admin_site)
        self.assertEqual(inline.get_inlines(REQUEST, None), ('a',))

    def test_generictabularinline_has_get_inlines(self):

        class MyGenericInline(GenericTabularInline):
            model = Media
            inlines = ['x', 'y']
        inline = MyGenericInline(Episode, admin_site)
        self.assertEqual(inline.get_inlines(REQUEST, None), ['x', 'y'])

    def test_tabularinline_inlines_list_returned(self):

        class MyInline(admin.TabularInline):
            model = Media
            inlines = ['one']
        inline = MyInline(Episode, admin_site)
        self.assertIsInstance(inline.get_inlines(REQUEST, None), list)
        self.assertEqual(inline.get_inlines(REQUEST, None), ['one'])

    def test_tabularinline_inlines_tuple_returned(self):

        class MyInline(admin.TabularInline):
            model = Media
            inlines = ('only',)
        inline = MyInline(Episode, admin_site)
        self.assertIsInstance(inline.get_inlines(REQUEST, None), tuple)
        self.assertEqual(inline.get_inlines(REQUEST, None), ('only',))

    def test_inline_modeladmin_get_inlines_direct_call(self):

        class DirectInline(admin.TabularInline):
            model = Media
            inlines = ('direct',)
        inst = DirectInline(Episode, admin_site)
        self.assertEqual(inst.get_inlines(REQUEST, object()), ('direct',))

    def test_basemodeladmin_subclass_has_get_inlines(self):
        from django.contrib.admin.options import BaseModelAdmin

        class BM(BaseModelAdmin):
            inlines = ('bm',)
        bm = BM()
        self.assertEqual(bm.get_inlines(REQUEST, None), ('bm',))

    def test_get_inlines_accepts_obj_arg(self):

        class MyInline(admin.TabularInline):
            model = Media
            inlines = ('objtest',)
        inline = MyInline(Episode, admin_site)
        sentinel = object()
        self.assertEqual(inline.get_inlines(REQUEST, sentinel), ('objtest',))

    def test_get_inlines_on_inline_respects_class_attr(self):

        class CustomInline(admin.TabularInline):
            model = Media
            inlines = []
        inst = CustomInline(Episode, admin_site)
        self.assertEqual(inst.get_inlines(REQUEST, None), [])

from inspect import signature
from types import GeneratorType
from django import forms
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin, ModelAdmin
from django.test import RequestFactory, SimpleTestCase
from .models import Episode, Media

class GetInlinesRegressionTests(SimpleTestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.site = AdminSite()

    def test_01_base_model_admin_has_get_inlines(self):
        self.assertTrue(hasattr(BaseModelAdmin, 'get_inlines'))
        self.assertTrue(callable(getattr(BaseModelAdmin, 'get_inlines')))

    def test_02_inline_model_admin_inherits_get_inlines(self):

        class DummyInline(InlineModelAdmin):
            model = Media
        inst = DummyInline(Episode, self.site)
        self.assertTrue(hasattr(inst, 'get_inlines'))
        self.assertTrue(callable(getattr(inst, 'get_inlines')))

    def test_10_baseclass_method_is_callable_on_instances(self):

        class SomeInline(admin.TabularInline):
            model = Media

        class MyInline(InlineModelAdmin):
            model = Media
        mi = MyInline(Episode, self.site)
        ma = ModelAdmin(Episode, self.site)
        self.assertTrue(callable(mi.get_inlines))
        self.assertTrue(callable(ma.get_inlines))

from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.contenttypes.admin import GenericTabularInline
from django.test import SimpleTestCase
from .models import Episode, Media

class GetInlinesBaseTests(SimpleTestCase):

    def setUp(self):
        self.site = AdminSite()

        class Req:
            pass
        self.request = Req()
        self.obj = object()

    def test_base_modeladmin_has_get_inlines(self):
        self.assertTrue(hasattr(BaseModelAdmin, 'get_inlines'))

from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin
from django.contrib.admin.sites import AdminSite
from django.test import SimpleTestCase, RequestFactory

class BaseGetInlinesRegressionTests(SimpleTestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.obj = object()

    def test_basemodeladmin_get_inlines_returns_list(self):

        class MyBaseAdmin(BaseModelAdmin):
            pass
        admin = MyBaseAdmin()
        admin.inlines = ['A', 'B']
        self.assertEqual(admin.get_inlines(self.request, self.obj), ['A', 'B'])

    def test_basemodeladmin_get_inlines_returns_tuple(self):

        class MyBaseAdmin(BaseModelAdmin):
            pass
        admin = MyBaseAdmin()
        admin.inlines = ('X', 'Y')
        self.assertEqual(admin.get_inlines(self.request, None), ('X', 'Y'))

    def test_basemodeladmin_get_inlines_empty(self):

        class MyBaseAdmin(BaseModelAdmin):
            pass
        admin = MyBaseAdmin()
        admin.inlines = ()
        self.assertEqual(admin.get_inlines(self.request, None), ())

    def test_basemodeladmin_get_inlines_with_None_value(self):

        class MyBaseAdmin(BaseModelAdmin):
            pass
        admin = MyBaseAdmin()
        admin.inlines = None
        self.assertIsNone(admin.get_inlines(self.request, self.obj))

class InlineModelAdminGetInlinesRegressionTests(SimpleTestCase):

    def setUp(self):
        self.request = RequestFactory().get('/')
        self.site = AdminSite()
        DummyMeta = type('DummyMeta', (), {})()
        DummyModel = type('DummyModel', (), {'_meta': DummyMeta})

    def test_basemodeladmin_and_inlinemodeladmin_independent_instances(self):

        class MyBaseAdmin(BaseModelAdmin):
            pass
        admin1 = MyBaseAdmin()
        admin2 = MyBaseAdmin()
        admin1.inlines = ['A']
        admin2.inlines = ['B']
        self.assertEqual(admin1.get_inlines(self.request, None), ['A'])
        self.assertEqual(admin2.get_inlines(self.request, None), ['B'])

from django.contrib.admin.options import BaseModelAdmin, ModelAdmin, InlineModelAdmin
from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin, ModelAdmin, InlineModelAdmin
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, SimpleTestCase, TestCase
from django.forms.models import modelform_factory
from django.db import models
from django.contrib.auth.models import User

class GetInlinesDefaultTest(SimpleTestCase):

    def test_basemodeladmin_has_get_inlines(self):
        self.assertTrue(hasattr(BaseModelAdmin, 'get_inlines'), 'BaseModelAdmin must define get_inlines')

    def test_inlinemodeladmin_inherits_get_inlines(self):
        self.assertTrue(hasattr(InlineModelAdmin, 'get_inlines'), 'InlineModelAdmin must inherit get_inlines from BaseModelAdmin')