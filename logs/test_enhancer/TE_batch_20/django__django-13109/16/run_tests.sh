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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateManagerTests._make_article model_forms.test_models_llm.ForeignKeyValidateManagerTests.setUp model_forms.test_models_llm.ForeignKeyValidateManagerTests.test_clean_fields_with_pk_excluded_by_default_manager_passes model_forms.test_models_llm.ForeignKeyValidateManagerTests.test_field_validate_direct_with_instance_does_not_raise model_forms.test_models_llm.ForeignKeyValidateManagerTests.test_field_validate_direct_with_pk_does_not_raise model_forms.test_models_llm.ForeignKeyValidateManagerTests.test_full_clean_raises_for_nonexistent_pk model_forms.test_models_llm.ForeignKeyValidateManagerTests.test_full_clean_with_instance_excluded_by_default_manager_passes model_forms.test_models_llm.ForeignKeyValidateManagerTests.test_full_clean_with_pk_excluded_by_default_manager_passes model_forms.test_models_llm.ForeignKeyValidateManagerTests.test_model_form_with_base_manager_queryset_passes_for_archived_pk model_forms.test_models_llm.ForeignKeyValidateManagerTests.test_model_form_without_query_set_fails_for_archived_pk model_forms.test_models_llm.ForeignKeyValidateManagerTests.test_multiple_calls_to_validate_consistent model_forms.test_models_llm.ForeignKeyValidateManagerTests.test_validate_after_deleting_target_raises
coverage json -o coverage.json
: '>>>>> End Test Output'
