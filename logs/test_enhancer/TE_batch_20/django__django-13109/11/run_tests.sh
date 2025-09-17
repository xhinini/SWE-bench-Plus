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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.setUp model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_assigning_related_instance_and_full_clean model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_direct_field_validate_uses_base_manager model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_field_validate_with_model_instance_value model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_full_clean_allows_archived_writer model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_full_clean_with_archived_writer_and_existing_non_default_queryset_in_form model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_modelform_invalid_for_nonexistent_writer model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_modelform_is_valid_with_archived_writer_when_query_using_base_manager model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_one_to_one_field_full_clean_uses_base_manager model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_validate_raises_for_nonexistent_value_direct_call
coverage json -o coverage.json
: '>>>>> End Test Output'
