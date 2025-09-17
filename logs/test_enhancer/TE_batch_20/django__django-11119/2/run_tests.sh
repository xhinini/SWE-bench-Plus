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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 template_tests.test_engine_llm.EngineRegressionTests.setUp template_tests.test_engine_llm.EngineRegressionTests.test_template_render_with_dict_raises_attribute_error template_tests.test_engine_llm.EngineRegressionTests.test_template_render_with_int_raises_attribute_error template_tests.test_engine_llm.EngineRegressionTests.test_template_render_with_list_raises_attribute_error template_tests.test_engine_llm.EngineRegressionTests.test_template_render_with_none_raises_attribute_error template_tests.test_engine_llm.EngineRegressionTests.test_template_render_with_string_raises_attribute_error template_tests.test_engine_llm.EngineRegressionTests.test_template_render_with_tuple_raises_attribute_error
coverage json -o coverage.json
: '>>>>> End Test Output'
