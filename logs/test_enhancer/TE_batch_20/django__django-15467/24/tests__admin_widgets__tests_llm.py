from django.test import SimpleTestCase
from django.contrib import admin
from django.db.models import ForeignKey
from django.contrib.admin import widgets
from django import forms
from .models import Inventory, Event