from django import forms
from django.test import SimpleTestCase
from django.contrib import admin
from django.contrib.admin import widgets
from django.db.models import ManyToManyField
from django.utils.translation import gettext as _
from .models import Band, Advisor