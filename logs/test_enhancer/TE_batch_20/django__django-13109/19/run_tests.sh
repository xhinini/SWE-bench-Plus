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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateTests.setUp model_forms.test_models_llm.ForeignKeyValidateTests.test_parent_link_skips_validation model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_accepts_archived_writer_using_base_manager model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_accepts_model_instance_value_instead_of_pk model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_allows_none_value model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_calls_complex_filter_with_limit_choices_to_callable model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_error_message_contains_field_and_model model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_prefers_base_manager_over_default_manager model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_rejects_nonexistent_writer_raises_validationerror model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_uses_router_db_for_read_called model_forms.test_models_llm.ForeignKeyValidateTests.test_validation_error_params_include_expected_values
coverage json -o coverage.json
: '>>>>> End Test Output'
