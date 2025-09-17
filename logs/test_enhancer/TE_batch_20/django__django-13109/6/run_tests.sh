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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.setUp model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_fk_validate_accepts_string_pk_value model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_fk_validate_allows_archived_using_instance_on_article model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_fk_validate_allows_archived_using_pk_on_article model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_fk_validate_on_book_accepts_archived_author model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_fk_validate_raises_for_nonexistent_pk_article model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_form_rejects_archived_using_default_queryset model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_modelform_allows_archived_writer_if_queryset_overridden_to_base_manager model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_one_to_one_validate_allows_archived_using_instance_on_writerprofile model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_one_to_one_validate_allows_archived_using_pk_on_writerprofile model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_uses_base_manager_when_limit_choices_to_present
coverage json -o coverage.json
: '>>>>> End Test Output'
