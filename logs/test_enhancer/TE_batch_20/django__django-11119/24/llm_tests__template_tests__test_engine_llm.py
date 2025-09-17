from django.template import Context
from django.template import Context, TemplateDoesNotExist
from django.template.engine import Engine
from django.test import SimpleTestCase
from .utils import TEMPLATE_DIR, ROOT
import os
OTHER_DIR = os.path.join(ROOT, 'other_templates')