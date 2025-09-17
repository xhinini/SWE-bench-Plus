from django import forms
from django.contrib import admin
from django.contrib.admin import widgets as admin_widgets
from django import forms
from django.contrib import admin
from django.test import SimpleTestCase
from django.contrib.admin import widgets
from .models import Band
from django.contrib.admin import widgets as admin_widgets

def _unwrap_widget(field):
    """
    Helper to get the underlying widget (unwrapping RelatedFieldWidgetWrapper
    if present).
    """
    w = field.widget
    if isinstance(w, admin_widgets.RelatedFieldWidgetWrapper):
        return w.widget
    return w

from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.forms import CheckboxSelectMultiple
from django.test import SimpleTestCase
from django.db.models import ManyToManyField
from .models import Band

def _unwrap_widget(field):
    widget = field.widget
    if isinstance(widget, widgets.RelatedFieldWidgetWrapper):
        return widget.widget
    return widget