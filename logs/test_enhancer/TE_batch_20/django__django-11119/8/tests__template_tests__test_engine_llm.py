import os
from django.template import Context
from django.template.engine import Engine
from django.test import SimpleTestCase
from .utils import TEMPLATE_DIR

class TemplateRenderDictRejectionTests(SimpleTestCase):

    def test_template_render_from_string_with_dict_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR], autoescape=True)
        template = engine.from_string('obj:{{ obj }}')
        with self.assertRaises(AttributeError):
            template.render({'obj': '<script>'})

    def test_template_render_get_template_with_dict_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR], autoescape=True)
        template = engine.get_template('test_context.html')
        with self.assertRaises(AttributeError):
            template.render({'obj': '<script>'})

    def test_template_render_from_string_with_dict_autoescape_false_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR], autoescape=False)
        template = engine.from_string('obj:{{ obj }}')
        with self.assertRaises(AttributeError):
            template.render({'obj': '<script>'})

    def test_template_render_get_template_with_dict_autoescape_false_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR], autoescape=False)
        template = engine.get_template('test_context.html')
        with self.assertRaises(AttributeError):
            template.render({'obj': '<script>'})

    def test_template_render_from_string_with_empty_dict_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR])
        template = engine.from_string('x:{{ x }}')
        with self.assertRaises(AttributeError):
            template.render({})

    def test_template_render_get_template_with_non_string_value_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR])
        template = engine.get_template('test_context.html')
        with self.assertRaises(AttributeError):
            template.render(42)

from django.template import Context, Template
from django.template.engine import Engine
from django.test import SimpleTestCase
from .utils import TEMPLATE_DIR

class EngineRegressionTests(SimpleTestCase):

    def setUp(self):
        self.engine = Engine(dirs=[TEMPLATE_DIR])

    def test_template_render_with_dict_raises_attribute_error(self):
        template = Template('{{ name }}')
        with self.assertRaises(AttributeError):
            template.render({'name': 'value'})

    def test_template_render_with_list_raises_attribute_error(self):
        template = Template('{{ name }}')
        with self.assertRaises(AttributeError):
            template.render(['a', 'b'])

    def test_template_render_with_string_raises_attribute_error(self):
        template = Template('{{ name }}')
        with self.assertRaises(AttributeError):
            template.render('not-a-context')

    def test_template_render_with_none_raises_attribute_error(self):
        template = Template('{{ name }}')
        with self.assertRaises(AttributeError):
            template.render(None)

    def test_template_render_with_int_raises_attribute_error(self):
        template = Template('{{ name }}')
        with self.assertRaises(AttributeError):
            template.render(123)

    def test_template_render_with_tuple_raises_attribute_error(self):
        template = Template('{{ name }}')
        with self.assertRaises(AttributeError):
            template.render(('a',))

import os
from django.template import Context
from django.template.engine import Engine
from django.test import SimpleTestCase
from .utils import TEMPLATE_DIR

class EngineAdditionalTests(SimpleTestCase):

    def setUp(self):
        self.engine = Engine(dirs=[TEMPLATE_DIR])

    def test_template_render_raises_with_dict_context_basic(self):
        t = self.engine.from_string('obj:{{ obj }}')
        with self.assertRaises(AttributeError):
            t.render({'obj': '<b>'})

    def test_template_render_raises_with_dict_context_from_engine(self):
        engine = Engine(dirs=[TEMPLATE_DIR])
        t = engine.from_string('obj:{{ obj }}')
        with self.assertRaises(AttributeError):
            t.render({'obj': '<i>'})

    def test_template_render_raises_with_list_context(self):
        t = self.engine.from_string('obj:{{ obj }}')
        with self.assertRaises(AttributeError):
            t.render(['not', 'a', 'Context'])

    def test_template_render_raises_with_int_context(self):
        t = self.engine.from_string('val:{{ value }}')
        with self.assertRaises(AttributeError):
            t.render(123)

    def test_template_render_raises_with_none_context(self):
        t = self.engine.from_string('val:{{ value }}')
        with self.assertRaises(AttributeError):
            t.render(None)

from django.template.base import Template
from django.test import SimpleTestCase
from django.template.base import Template

class TemplateRenderWithoutEngineTests(SimpleTestCase):

    def test_render_with_simple_dict_raises_about_render_context(self):
        tpl = Template('Hello {{ name }}!')
        with self.assertRaisesMessage(AttributeError, 'render_context'):
            tpl.render({'name': 'world'})

    def test_render_with_empty_dict_raises_about_render_context(self):
        tpl = Template('Value: {{ value }}')
        with self.assertRaisesMessage(AttributeError, 'render_context'):
            tpl.render({})

    def test_render_with_list_raises_about_render_context(self):
        tpl = Template('Item: {{ 0 }}')
        with self.assertRaisesMessage(AttributeError, 'render_context'):
            tpl.render(['a', 'b'])

    def test_render_with_custom_object_raises_about_render_context(self):

        class PlainObject:
            pass
        tpl = Template('Attr: {{ x }}')
        with self.assertRaisesMessage(AttributeError, 'render_context'):
            tpl.render(PlainObject())

    def test_render_with_int_raises_about_render_context(self):
        tpl = Template('Number: {{ nothing }}')
        with self.assertRaisesMessage(AttributeError, 'render_context'):
            tpl.render(123)

    def test_render_with_none_raises_about_render_context(self):
        tpl = Template('None: {{ nothing }}')
        with self.assertRaisesMessage(AttributeError, 'render_context'):
            tpl.render(None)

    def test_render_with_tuple_raises_about_render_context(self):
        tpl = Template('Tuple: {{ 0 }}')
        with self.assertRaisesMessage(AttributeError, 'render_context'):
            tpl.render(('x',))

    def test_render_with_set_raises_about_render_context(self):
        tpl = Template('Set: {{ 0 }}')
        with self.assertRaisesMessage(AttributeError, 'render_context'):
            tpl.render(set([1, 2]))

    def test_render_with_bytes_raises_about_render_context(self):
        tpl = Template('Bytes: {{ nothing }}')
        with self.assertRaisesMessage(AttributeError, 'render_context'):
            tpl.render(b'bytes')

from django.template import TemplateDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from django.template import Context, TemplateDoesNotExist
from django.template.engine import Engine
from django.test import SimpleTestCase
from .utils import TEMPLATE_DIR

class RenderToStringAutoescapeTests(SimpleTestCase):

    def setUp(self):
        self.engine = Engine(dirs=[TEMPLATE_DIR])

class SelectTemplateAndGetTemplateTests(SimpleTestCase):

    def setUp(self):
        self.engine = Engine(dirs=[TEMPLATE_DIR])

from collections import UserDict
import os
from collections import UserDict
from django.template import Context
from django.template.engine import Engine
from django.test import SimpleTestCase
from .utils import TEMPLATE_DIR

class EngineAutoescapeRegressionTests(SimpleTestCase):

    def setUp(self):
        self.template_name = 'test_context.html'

import os
from django.core.exceptions import ImproperlyConfigured
from django.template import Context, Template, TemplateDoesNotExist
from django.template.engine import Engine
from django.test import SimpleTestCase, override_settings
from .utils import ROOT, TEMPLATE_DIR
OTHER_DIR = os.path.join(ROOT, 'other_templates')


class SelectTemplateTests(SimpleTestCase):

    def setUp(self):
        self.engine = Engine(dirs=[TEMPLATE_DIR])

class TemplateRenderDirectnessTests(SimpleTestCase):

    def test_template_render_direct_without_engine_raises_on_dict(self):
        t = Template('obj:{{ obj }}')
        with self.assertRaisesMessage(AttributeError, 'render_context'):
            t.render({'obj': 'value'})

    def test_template_from_engine_render_with_dict_without_wrapping_raises(self):
        engine = Engine(dirs=[TEMPLATE_DIR])
        t = engine.from_string('obj:{{ obj }}')
        with self.assertRaisesMessage(AttributeError, 'render_context'):
            t.render({'obj': '<x>'})

from collections import UserDict
from types import MappingProxyType
import os
from collections import UserDict
from types import MappingProxyType
from django.template import Context
from django.template.engine import Engine
from django.test import SimpleTestCase
from .utils import TEMPLATE_DIR

class RenderToStringAutoescapeRegressionTests(SimpleTestCase):

    def setUp(self):
        self.template_name = 'test_context.html'
        self.engine_default = Engine(dirs=[TEMPLATE_DIR])
        self.engine_no_auto = Engine(dirs=[TEMPLATE_DIR], autoescape=False)