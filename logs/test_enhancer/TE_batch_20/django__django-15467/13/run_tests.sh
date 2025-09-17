#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_widgets.tests_llm.RadioEmptyLabelRegressionTests.test_formfield_overrides_empty_string_preserved admin_widgets.tests_llm.RadioEmptyLabelRegressionTests.test_formfield_overrides_false_preserved admin_widgets.tests_llm.RadioEmptyLabelRegressionTests.test_formfield_overrides_none_preserved admin_widgets.tests_llm.RadioEmptyLabelRegressionTests.test_formfield_overrides_zero_preserved admin_widgets.tests_llm.RadioEmptyLabelRegressionTests.test_kwargs_empty_string_preserved admin_widgets.tests_llm.RadioEmptyLabelRegressionTests.test_kwargs_false_preserved admin_widgets.tests_llm.RadioEmptyLabelRegressionTests.test_kwargs_none_preserved admin_widgets.tests_llm.RadioEmptyLabelRegressionTests.test_kwargs_override_formfield_overrides_empty_string
coverage json -o coverage.json
: '>>>>> End Test Output'
