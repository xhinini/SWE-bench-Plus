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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_engine_llm.EngineRenderToStringAutoescapeTests.setUp template_tests.test_engine_llm.TemplateRenderWithoutEngineTests.test_render_to_string_with_multiple_names_where_first_missing template_tests.test_engine_llm.TemplateRenderWithoutEngineTests.test_template_render_without_engine_raises_when_passed_plain_dict
coverage json -o coverage.json
: '>>>>> End Test Output'
