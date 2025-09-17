from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models
from .admin import site, ParentAdminTwoSearchFields, ChildAdmin
from .models import Parent, Child

class GetSearchResultsTests(TestCase):

    def _admin_for_parent(self):
        return ParentAdminTwoSearchFields(Parent, site)

from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.db import transaction
from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.db import transaction
from .models import Child, Parent, Band, Swallow, Event

class GetSearchResultsTests(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()
        self.parent1 = Parent.objects.create(name='Parent One')
        self.parent2 = Parent.objects.create(name='Parent Two')
        self.child_a = Child.objects.create(name='foo bar', age=5, parent=self.parent1)
        self.child_b = Child.objects.create(name='foo', age=7, parent=self.parent1)
        self.child_c = Child.objects.create(name='bar', age=9, parent=self.parent2)
        self.band1 = Band.objects.create(name='The Foo Band', nr_of_members=4)
        self.band2 = Band.objects.create(name='Bar Ensemble', nr_of_members=6)
        self.sw1 = Swallow.objects.create(origin='Africa', load=1, speed=10)
        self.sw2 = Swallow.objects.create(origin='Europe', load=2, speed=20)
        self.ev = Event.objects.create(date='2020-01-01')

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import AnonymousUser
from django.contrib.admin.options import ModelAdmin
from .admin import ParentAdmin, ParentAdminTwoSearchFields, DynamicSearchFieldsChildAdmin
from .models import Parent, Child

class SearchTermQueriesTests(TestCase):

    def setUp(self):
        self.parent1 = Parent.objects.create(name='Parent 1')
        Child.objects.create(name='Alice', age=5, parent=self.parent1)
        self.parent2 = Parent.objects.create(name='Parent 2')
        Child.objects.create(name='Bob', age=10, parent=self.parent2)
        self.parent3 = Parent.objects.create(name='Parent 3')
        Child.objects.create(name='Alice Bob', age=15, parent=self.parent3)
        self.parent4 = Parent.objects.create(name='Parent 4')
        Child.objects.create(name='Alice', age=6, parent=self.parent4)
        Child.objects.create(name='Bob', age=5, parent=self.parent4)
        self.request = DummyRequest()

from django.test import RequestFactory
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.db import transaction
from django.contrib.admin.options import ModelAdmin
from .models import Parent, Child

class GetSearchResultsTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.parent_bob = Parent.objects.create(name='Bob')
        self.parent_carol = Parent.objects.create(name='Carol')
        self.child1 = Child.objects.create(name='Alice', parent=self.parent_bob)
        self.child2 = Child.objects.create(name='Bobby', parent=self.parent_carol)
        self.child3 = Child.objects.create(name='Alice Bob', parent=self.parent_carol)
        self.child4 = Child.objects.create(name='Alice', parent=self.parent_carol)
        self.child5 = Child.objects.create(name='Alfred', parent=self.parent_bob)

from django.test import RequestFactory, TestCase
from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.http import urlencode
from .models import Parent, Child
from . import admin as test_admin_module

class SearchResultsTestCase(TestCase):

    def _get_request(self, path='/', method='GET', data=None):
        if method.upper() == 'GET':
            req = self.request_factory.get(path + ('?' + urlencode(data) if data else ''))
        else:
            req = self.request_factory.post(path, data or {})
        req.user = self.user
        return req

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from types import SimpleNamespace
from .admin import DynamicSearchFieldsChildAdmin, ParentAdminTwoSearchFields, site as test_site
from .models import Child, Parent

class ModelAdminSearchTests(TestCase):

    def _get_request(self):
        req = self.factory.get('/')
        req.user = self.user
        return req

from django.test import RequestFactory
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import AnonymousUser
from .admin import site
from .models import Parent, Child, Band, Genre
rf = RequestFactory()

class SearchTests(TestCase):

    def setUp(self):
        self.parent1 = Parent.objects.create(name='Parent One')
        self.child1 = Child.objects.create(name='Alice', age=30, parent=self.parent1)
        self.parent2 = Parent.objects.create(name='Parent Two')
        self.child2 = Child.objects.create(name='Alice Bob', age=40, parent=self.parent2)
        self.parent3 = Parent.objects.create(name='Parent Three')
        self.child3 = Child.objects.create(name='Bob Alice', age=25, parent=self.parent3)
        self.genre_rock = Genre.objects.create(name='Rock')
        self.genre_pop = Genre.objects.create(name='Pop')
        self.band1 = Band.objects.create(name='Band One', nr_of_members=4)
        self.band2 = Band.objects.create(name='Band Two', nr_of_members=6)
        self.band1.genres.add(self.genre_rock)
        self.band2.genres.add(self.genre_rock, self.genre_pop)
        self.request = rf.get('/')
        self.request.user = AnonymousUser()

from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db import transaction
from .models import Parent, Child, Band

class SearchResultsRegressionTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.admin_site = admin.AdminSite()

from django.test import TestCase
from django.contrib import admin
from django.test import TestCase
from django.contrib import admin
from django.db import connection
from django.db import reset_queries
from .models import Parent, Child, Band, Swallow
from .admin import ParentAdmin, ParentAdminTwoSearchFields, ConcertAdmin, site

class SearchRegressionTests(TestCase):

    def setUp(self):
        self.child_foo_10 = Child.objects.create(name='foo', age=10)
        self.child_foo_bar_10 = Child.objects.create(name='foo bar', age=10)
        self.child_bar_20 = Child.objects.create(name='bar', age=20)
        self.parent_a = Parent.objects.create(name='Parent A', child=self.child_foo_10)
        self.parent_b = Parent.objects.create(name='Parent B', child=self.child_foo_bar_10)
        self.parent_c = Parent.objects.create(name='Parent C', child=self.child_bar_20)

from django.test import TestCase
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Parent, Child
from django.test import TestCase
from django.contrib import admin
from django.contrib.admin import site as default_site
from django.contrib.admin.options import ModelAdmin
from django.db.models import Q
from .models import Parent, Child

class GetSearchResultsTests(TestCase):

    def setUp(self):
        self.site = admin.AdminSite(name='testsite')