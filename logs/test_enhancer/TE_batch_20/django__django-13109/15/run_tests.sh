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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.setUp model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_book_author_full_clean_accepts_archived_writer model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_default_manager_excludes_archived_but_base_manager_finds model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_field_validate_none_value_is_allowed model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_field_validate_raises_for_nonexistent_pk model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_field_validate_with_id_accepts_archived_writer model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_field_validate_with_instance_accepts_archived_writer model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_full_clean_accepts_archived_writer model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_modelform_accepts_archived_writer_when_queryset_set_to_base_manager model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_parent_link_one_to_one_field_skips_validation model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_called_directly_then_full_clean_behaves_same
coverage json -o coverage.json
: '>>>>> End Test Output'
