from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .admin import ParentAdmin, ParentAdminTwoSearchFields, ChildAdmin, BandCallableFilterAdmin, ConcertAdmin
from .models import Parent, Child, Band, Genre, Group
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.db import transaction
from .admin import ParentAdmin, ParentAdminTwoSearchFields, ChildAdmin, BandCallableFilterAdmin, ConcertAdmin
from .models import Parent, Child, Band, Genre, Group