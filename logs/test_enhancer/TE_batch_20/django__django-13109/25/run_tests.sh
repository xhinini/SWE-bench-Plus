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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.setUp model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_field_validate_accepts_instance_filtered_by_default_manager model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_field_validate_accepts_pk_filtered_by_default_manager model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_field_validate_rejects_nonexistent model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_full_clean_accepts_active_writer model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_full_clean_accepts_instance_for_object_filtered_by_default_manager model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_full_clean_accepts_pk_for_object_filtered_by_default_manager model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_full_clean_rejects_non_existent_pk model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_modelform_with_base_manager_allows_filtered_value_when_adjusted model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_modelform_with_default_manager_rejects_filtered_value model_forms.test_models_llm.[] (model_forms.test_models_llm.ArticleWriterForm)
coverage json -o coverage.json
: '>>>>> End Test Output'
