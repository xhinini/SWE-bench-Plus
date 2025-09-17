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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.tests_llm.ModelToDictPatchTests.setUpTestData model_forms.tests_llm.ModelToDictPatchTests.test_empty_fields_with_nonempty_exclude_still_empty model_forms.tests_llm.ModelToDictPatchTests.test_empty_tuple_with_empty_exclude model_forms.tests_llm.ModelToDictPatchTests.test_exclude_list_excludes_fields model_forms.tests_llm.ModelToDictPatchTests.test_fields_accepted_as_set_and_empty_set_returns_empty model_forms.tests_llm.ModelToDictPatchTests.test_fields_and_exclude_exclude_wins model_forms.tests_llm.ModelToDictPatchTests.test_fields_empty_list_returns_empty_dict model_forms.tests_llm.ModelToDictPatchTests.test_fields_empty_tuple_returns_empty_dict model_forms.tests_llm.ModelToDictPatchTests.test_fields_none_returns_all_editable_fields model_forms.tests_llm.ModelToDictPatchTests.test_fields_specific_returns_only_those_fields model_forms.tests_llm.ModelToDictPatchTests.test_many_to_many_field_returns_list_snapshot_when_requested
coverage json -o coverage.json
: '>>>>> End Test Output'
