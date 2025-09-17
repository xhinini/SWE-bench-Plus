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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_engine_llm.RenderToStringAutoescapeTests.setUp template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_context_instance_autoescape_overrides_engine_false template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_context_instance_autoescape_overrides_engine_true template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_context_subclass_is_recognized_and_preserves_autoescape template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_dict_subclass_is_treated_like_plain_mapping_and_uses_engine_autoescape template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_engine_autoescape_false_no_escape template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_engine_autoescape_true_escapes template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_select_template_with_list_and_context_overrides_engine template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_select_template_with_list_and_context_overrides_engine_reverse template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_select_template_with_list_and_dict_uses_engine_autoescape_false template_tests.test_engine_llm.RenderToStringAutoescapeTests.test_select_template_with_list_and_dict_uses_engine_autoescape_true
coverage json -o coverage.json
: '>>>>> End Test Output'
