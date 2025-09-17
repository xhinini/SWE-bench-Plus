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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateTests.test_full_clean_allows_archived_writer_by_pk model_forms.test_models_llm.ForeignKeyValidateTests.test_full_clean_allows_archived_writer_with_instance model_forms.test_models_llm.ForeignKeyValidateTests.test_full_clean_rejects_nonexistent_and_accepts_existing_archived model_forms.test_models_llm.ForeignKeyValidateTests.test_modelform_rejects_archived_writer_but_model_validation_accepts model_forms.test_models_llm.ForeignKeyValidateTests.test_one_to_one_full_clean_with_instance model_forms.test_models_llm.ForeignKeyValidateTests.test_one_to_one_validate_accepts_archived_writer_pk model_forms.test_models_llm.ForeignKeyValidateTests.test_parent_link_field_skips_validation model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_allows_archived_writer_by_pk_direct_validate_call model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_rejects_nonexistent_pk model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_with_none_returns_without_error
coverage json -o coverage.json
: '>>>>> End Test Output'
