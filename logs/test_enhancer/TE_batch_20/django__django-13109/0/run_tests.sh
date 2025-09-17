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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.setUp model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_field_validate_accepts_model_instance_value model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_field_validate_accepts_pk_from_base_manager model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_field_validate_accepts_pk_when_instance_is_saved model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_full_clean_accepts_base_manager_value model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_raises_for_nonexistent_pk model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_returns_early_for_parent_link model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_returns_for_none_value model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_with_live_writer_pk_is_ok model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_with_model_instance_value_after_saving_article model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validation_error_message_includes_model_and_field
coverage json -o coverage.json
: '>>>>> End Test Output'
