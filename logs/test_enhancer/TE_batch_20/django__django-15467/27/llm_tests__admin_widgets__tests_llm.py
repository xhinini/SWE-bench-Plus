from django.test import TestCase, override_settings
from django import forms
from django.contrib import admin
from django.db import models as dj_models
from .models import Inventory, Event
from django.db.models import ForeignKey