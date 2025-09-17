from django.template import Template
from django.core.exceptions import ImproperlyConfigured, TemplateDoesNotExist
from django.template import Context
from django.template.engine import Engine
from django.test import SimpleTestCase
from .utils import TEMPLATE_DIR