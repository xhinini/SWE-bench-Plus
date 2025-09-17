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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateUsesBaseManagerTests._assert_validate_passes model_forms.test_models_llm.ForeignKeyValidateUsesBaseManagerTests.setUp model_forms.test_models_llm.ForeignKeyValidateUsesBaseManagerTests.test_validate_after_changing_archived_flag_to_true model_forms.test_models_llm.ForeignKeyValidateUsesBaseManagerTests.test_validate_allows_archived_subclass_instance_pk model_forms.test_models_llm.ForeignKeyValidateUsesBaseManagerTests.test_validate_allows_archived_writer_with_int_pk model_forms.test_models_llm.ForeignKeyValidateUsesBaseManagerTests.test_validate_allows_archived_writer_with_model_instance model_forms.test_models_llm.ForeignKeyValidateUsesBaseManagerTests.test_validate_allows_archived_writer_with_str_pk model_forms.test_models_llm.ForeignKeyValidateUsesBaseManagerTests.test_validate_multiple_calls_do_not_change_outcome model_forms.test_models_llm.ForeignKeyValidateUsesBaseManagerTests.test_validate_with_arbitrary_model_instance_object model_forms.test_models_llm.ForeignKeyValidateUsesBaseManagerTests.test_validate_with_large_number_of_calls model_forms.test_models_llm.ForeignKeyValidateUsesBaseManagerTests.test_validate_with_none_model_instance_argument model_forms.test_models_llm.ForeignKeyValidateUsesBaseManagerTests.test_validate_with_pk_of_object_created_via_subclass_then_accessed_as_parent
coverage json -o coverage.json
: '>>>>> End Test Output'
