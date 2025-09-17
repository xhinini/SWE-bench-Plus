#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_engine_llm.RenderToStringAutoescapeTests.setUp template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_autoescape_false_for_dict_context template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_autoescape_false_with_template_list_selection template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_default_autoescape_true_for_dict_context template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_preserve_context_instance_autoescape_false template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_preserve_context_instance_autoescape_true_overrides_engine_false template_tests.test_engine_llm.TemplateRenderAPITests.setUp template_tests.test_engine_llm.TemplateRenderAPITests.test_render_to_string_with_context_subclass_preserves_autoescape template_tests.test_engine_llm.TemplateRenderAPITests.test_select_template_with_list_preserves_autoescape_for_dict template_tests.test_engine_llm.TemplateRenderAPITests.test_template_class_render_rejects_plain_mapping template_tests.test_engine_llm.TemplateRenderAPITests.test_template_from_string_render_rejects_plain_mapping
coverage json -o coverage.json
: '>>>>> End Test Output'
