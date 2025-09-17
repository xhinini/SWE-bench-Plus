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