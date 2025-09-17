from django.template.defaultfilters import join
from django.template import Template
from django.test import SimpleTestCase
from django.utils.safestring import mark_safe, SafeData
from ..utils import setup