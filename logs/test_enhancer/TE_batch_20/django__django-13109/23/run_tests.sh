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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyBaseManagerTests.test_default_manager_filters_out_archived_confirm model_forms.test_models_llm.ForeignKeyBaseManagerTests.test_field_validate_uses_base_manager_includes_archived model_forms.test_models_llm.ForeignKeyBaseManagerTests.test_field_validate_with_to_field_uses_base_manager model_forms.test_models_llm.ForeignKeyBaseManagerTests.test_full_clean_uses_base_manager_includes_archived model_forms.test_models_llm.ForeignKeyBaseManagerTests.test_full_clean_with_to_field_uses_base_manager model_forms.test_models_llm.ForeignKeyBaseManagerTests.test_multiple_archived_entries_non_pk_validate model_forms.test_models_llm.ForeignKeyBaseManagerTests.test_validate_after_creating_via_default_manager_fails_but_base_ok model_forms.test_models_llm.ForeignKeyBaseManagerTests.test_validate_none_value_early_return model_forms.test_models_llm.ForeignKeyBaseManagerTests.test_validate_with_object_instance_value model_forms.test_models_llm.ForeignKeyBaseManagerTests.test_validation_raises_when_base_manager_has_no_match model_forms.test_models_llm.register_and_create_models model_forms.test_models_llm.unregister_and_delete_models
coverage json -o coverage.json
: '>>>>> End Test Output'
