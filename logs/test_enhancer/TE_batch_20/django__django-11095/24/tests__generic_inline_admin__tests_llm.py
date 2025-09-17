from django.contrib import admin
from django.contrib.admin.options import BaseModelAdmin, InlineModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.test import SimpleTestCase
from .tests import request