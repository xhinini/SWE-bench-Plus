from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib import admin
from django.db import models
from .admin import site, ParentAdminTwoSearchFields, ChildAdmin
from .models import Parent, Child

class GetSearchResultsTests(TestCase):

    def _admin_for_parent(self):
        return ParentAdminTwoSearchFields(Parent, site)