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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.tests_llm.ModelToDictRegressionTests.setUpTestData model_forms.tests_llm.ModelToDictRegressionTests.test_empty_list_fields_returns_empty_dict model_forms.tests_llm.ModelToDictRegressionTests.test_empty_set_fields_returns_empty_dict model_forms.tests_llm.ModelToDictRegressionTests.test_empty_tuple_fields_returns_empty_dict model_forms.tests_llm.ModelToDictRegressionTests.test_exclude_overrides_fields model_forms.tests_llm.ModelToDictRegressionTests.test_fields_none_returns_all_editable_fields model_forms.tests_llm.ModelToDictRegressionTests.test_fields_single_field_returns_only_that_field
coverage json -o coverage.json
: '>>>>> End Test Output'
