from django.contrib import admin
from django.contrib.admin import widgets
from django import forms
from django.test import SimpleTestCase
from django.db.models import ForeignKey
from .models import Inventory, Profile