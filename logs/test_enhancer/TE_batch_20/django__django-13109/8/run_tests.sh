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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.RelatedFieldValidationTests.setUp model_forms.test_models_llm.RelatedFieldValidationTests.test_foreignkey_applies_limit_choices_to_callable_rejects_archived model_forms.test_models_llm.RelatedFieldValidationTests.test_foreignkey_applies_limit_choices_to_callable_returning_q_rejects_archived model_forms.test_models_llm.RelatedFieldValidationTests.test_foreignkey_applies_limit_choices_to_dict_rejects_archived model_forms.test_models_llm.RelatedFieldValidationTests.test_foreignkey_full_clean_accepts_archived_created_via_base_manager_using_id model_forms.test_models_llm.RelatedFieldValidationTests.test_foreignkey_full_clean_accepts_archived_created_via_base_manager_using_object model_forms.test_models_llm.RelatedFieldValidationTests.test_foreignkey_full_clean_rejects_nonexistent_id_raises_validation_error model_forms.test_models_llm.RelatedFieldValidationTests.test_modelform_field_is_more_restrictive_due_to_default_manager_queryset model_forms.test_models_llm.RelatedFieldValidationTests.test_one_to_one_full_clean_accepts_archived model_forms.test_models_llm.RelatedFieldValidationTests.test_parent_link_skips_validation model_forms.test_models_llm.RelatedFieldValidationTests.test_router_db_for_read_is_called_during_validate
coverage json -o coverage.json
: '>>>>> End Test Output'
