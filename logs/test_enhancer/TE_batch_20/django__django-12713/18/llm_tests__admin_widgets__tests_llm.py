from django import forms, admin
from django.test import SimpleTestCase
from django.contrib.admin import widgets
from .models import Band, Member
from django.contrib.admin.options import BaseModelAdmin