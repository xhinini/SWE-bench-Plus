from django.test import TestCase, RequestFactory
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import transaction
from .models import Parent, Child, Band, Genre, Group, Member
from .admin import ParentAdmin, ParentAdminTwoSearchFields, ChildAdmin, ConcertAdmin