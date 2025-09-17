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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateTests.setUp model_forms.test_models_llm.ForeignKeyValidateTests.test_field_validate_allows_archived_writer model_forms.test_models_llm.ForeignKeyValidateTests.test_field_validate_raises_for_nonexistent model_forms.test_models_llm.ForeignKeyValidateTests.test_full_clean_allows_archived_writer model_forms.test_models_llm.ForeignKeyValidateTests.test_modelform_validation_allows_archived_when_queryset_set_to_base_manager model_forms.test_models_llm.ForeignKeyValidateTests.test_parent_link_short_circuits_validation model_forms.test_models_llm.ForeignKeyValidateTests.test_router_db_for_read_called_with_instance model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_accepts_string_pk_values model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_none_is_accepted model_forms.test_models_llm.ForeignKeyValidateTests.test_validation_error_contains_model_name_and_field
coverage json -o coverage.json
: '>>>>> End Test Output'
