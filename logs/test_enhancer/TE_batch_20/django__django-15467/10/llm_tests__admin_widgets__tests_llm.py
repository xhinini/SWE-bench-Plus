from django.contrib import admin
from django.contrib.admin import widgets
from django import forms
from django.contrib import admin
from django.test import SimpleTestCase
from django.utils.translation import gettext as _
from django.db.models import ForeignKey
from tests.admin_widgets.models import Inventory, Event
from django.contrib.admin import widgets