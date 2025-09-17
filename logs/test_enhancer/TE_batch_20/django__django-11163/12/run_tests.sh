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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.tests_llm.ModelToDictRegressionTests.setUpTestData model_forms.tests_llm.ModelToDictRegressionTests.test_exclude_empty_list_equivalent_to_no_exclude model_forms.tests_llm.ModelToDictRegressionTests.test_exclude_removes_fields_from_full_set model_forms.tests_llm.ModelToDictRegressionTests.test_fields_empty_list_returns_empty_dict model_forms.tests_llm.ModelToDictRegressionTests.test_fields_empty_list_with_exclude_nonempty_returns_empty model_forms.tests_llm.ModelToDictRegressionTests.test_fields_empty_tuple_returns_empty_dict model_forms.tests_llm.ModelToDictRegressionTests.test_fields_list_and_exclude_ignores_excluded model_forms.tests_llm.ModelToDictRegressionTests.test_fields_none_returns_all_fields model_forms.tests_llm.ModelToDictRegressionTests.test_fields_none_with_exclude_combination model_forms.tests_llm.ModelToDictRegressionTests.test_fields_specified_returns_only_those model_forms.tests_llm.ModelToDictRegressionTests.test_many_to_many_with_empty_fields_returns_empty
coverage json -o coverage.json
: '>>>>> End Test Output'
