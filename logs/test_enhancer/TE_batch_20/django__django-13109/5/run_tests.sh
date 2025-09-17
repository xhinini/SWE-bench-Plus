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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidationBaseManagerTests.setUp model_forms.test_models_llm.ForeignKeyValidationBaseManagerTests.test_clean_accepts_archived_writer_instance model_forms.test_models_llm.ForeignKeyValidationBaseManagerTests.test_clean_accepts_archived_writer_pk model_forms.test_models_llm.ForeignKeyValidationBaseManagerTests.test_clean_none_is_allowed model_forms.test_models_llm.ForeignKeyValidationBaseManagerTests.test_clean_raises_for_nonexistent_pk model_forms.test_models_llm.ForeignKeyValidationBaseManagerTests.test_modelform_invalid_with_default_queryset_that_filters_archived model_forms.test_models_llm.ForeignKeyValidationBaseManagerTests.test_modelform_valid_when_query_set_overridden_to_base_manager model_forms.test_models_llm.ForeignKeyValidationBaseManagerTests.test_validate_accepts_archived_writer_instance model_forms.test_models_llm.ForeignKeyValidationBaseManagerTests.test_validate_accepts_archived_writer_pk model_forms.test_models_llm.ForeignKeyValidationBaseManagerTests.test_validate_none_is_allowed model_forms.test_models_llm.ForeignKeyValidationBaseManagerTests.test_validate_raises_for_nonexistent_pk
coverage json -o coverage.json
: '>>>>> End Test Output'
