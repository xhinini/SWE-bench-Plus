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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.tests_llm.test_model_to_dict_fields_none_returns_all_editable_fields model_forms.tests_llm.test_model_to_dict_with_empty_fields_and_exclude_still_empty model_forms.tests_llm.test_model_to_dict_with_empty_fields_for_inherited_model_returns_empty model_forms.tests_llm.test_model_to_dict_with_empty_fields_on_many_to_many_returns_empty model_forms.tests_llm.test_model_to_dict_with_empty_frozenset_fields_returns_empty model_forms.tests_llm.test_model_to_dict_with_empty_list_fields_returns_empty model_forms.tests_llm.test_model_to_dict_with_empty_set_fields_returns_empty model_forms.tests_llm.test_model_to_dict_with_empty_tuple_fields_returns_empty model_forms.tests_llm.test_model_to_dict_with_explicit_single_field_returns_only_that_field model_forms.tests_llm.test_model_to_dict_with_nonexistent_field_in_fields_returns_empty
coverage json -o coverage.json
: '>>>>> End Test Output'
