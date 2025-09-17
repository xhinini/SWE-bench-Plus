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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.tests_llm.ModelToDictRegressionTests.test_empty_list_fields_returns_empty_for_betterwriter model_forms.tests_llm.ModelToDictRegressionTests.test_empty_list_fields_returns_empty_for_colourfulitem_with_m2m model_forms.tests_llm.ModelToDictRegressionTests.test_empty_list_fields_returns_empty_for_product model_forms.tests_llm.ModelToDictRegressionTests.test_empty_tuple_fields_returns_empty_for_betterwriter model_forms.tests_llm.ModelToDictRegressionTests.test_fields_empty_list_and_exclude_empty_list_returns_empty model_forms.tests_llm.ModelToDictRegressionTests.test_fields_empty_list_and_exclude_non_empty_ignores_exclude model_forms.tests_llm.ModelToDictRegressionTests.test_fields_list_and_exclude_combination_respects_exclude model_forms.tests_llm.ModelToDictRegressionTests.test_fields_none_returns_all_editable_fields_for_betterwriter model_forms.tests_llm.ModelToDictRegressionTests.test_fields_specified_returns_only_those_fields model_forms.tests_llm.ModelToDictRegressionTests.test_multiple_calls_with_empty_fields_are_consistent
coverage json -o coverage.json
: '>>>>> End Test Output'
