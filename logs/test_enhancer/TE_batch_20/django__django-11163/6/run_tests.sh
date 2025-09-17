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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.tests_llm.ModelToDictEmptyFieldsAdditionalTests.setUpTestData model_forms.tests_llm.ModelToDictEmptyFieldsAdditionalTests.test_model_to_dict_empty_list_with_exclude_still_empty model_forms.tests_llm.ModelToDictEmptyFieldsAdditionalTests.test_model_to_dict_explicit_fields_list_returns_only_those model_forms.tests_llm.ModelToDictEmptyFieldsAdditionalTests.test_model_to_dict_explicit_fields_tuple_returns_only_those model_forms.tests_llm.ModelToDictEmptyFieldsAdditionalTests.test_model_to_dict_fields_none_includes_all model_forms.tests_llm.ModelToDictEmptyFieldsAdditionalTests.test_model_to_dict_many_to_many_with_empty_iterables_returns_empty model_forms.tests_llm.ModelToDictEmptyFieldsAdditionalTests.test_model_to_dict_with_empty_frozenset_returns_empty model_forms.tests_llm.ModelToDictEmptyFieldsAdditionalTests.test_model_to_dict_with_empty_list_returns_empty model_forms.tests_llm.ModelToDictEmptyFieldsAdditionalTests.test_model_to_dict_with_empty_set_returns_empty model_forms.tests_llm.ModelToDictEmptyFieldsAdditionalTests.test_model_to_dict_with_empty_tuple_returns_empty
coverage json -o coverage.json
: '>>>>> End Test Output'
