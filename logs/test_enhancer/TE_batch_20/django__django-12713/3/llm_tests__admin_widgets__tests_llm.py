from django import forms
from django.test import SimpleTestCase
from django.contrib import admin
from django.contrib.admin import widgets as admin_widgets
from django.db.models import ManyToManyField
from .models import Band, Advisor