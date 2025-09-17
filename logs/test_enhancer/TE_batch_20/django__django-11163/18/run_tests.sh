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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.tests_llm.ModelToDictRegressionTests.setUpTestData model_forms.tests_llm.ModelToDictRegressionTests.test_empty_list_many_to_many_returns_empty_for_article model_forms.tests_llm.ModelToDictRegressionTests.test_empty_list_returns_empty_for_betterwriter model_forms.tests_llm.ModelToDictRegressionTests.test_empty_list_with_exclude_returns_empty_for_betterwriter model_forms.tests_llm.ModelToDictRegressionTests.test_empty_sequence_for_other_model_returns_empty model_forms.tests_llm.ModelToDictRegressionTests.test_empty_tuple_returns_empty_for_betterwriter model_forms.tests_llm.ModelToDictRegressionTests.test_fields_and_exclude_interaction model_forms.tests_llm.ModelToDictRegressionTests.test_fields_empty_with_empty_exclude_for_category model_forms.tests_llm.ModelToDictRegressionTests.test_fields_none_returns_all_editable_fields_for_betterwriter model_forms.tests_llm.ModelToDictRegressionTests.test_fields_subset_returns_only_requested_fields model_forms.tests_llm.ModelToDictRegressionTests.test_result_immutable_after_m2m_change_when_fields_empty
coverage json -o coverage.json
: '>>>>> End Test Output'
