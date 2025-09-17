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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.RelatedFieldBaseManagerTests.setUp model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_direct_validate_using_base_manager_created_via_base_manager model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_foreignkey_field_validate_article_saved_instance model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_foreignkey_field_validate_article_unsaved_instance model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_foreignkey_field_validate_book_instance model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_instance_full_clean_article_with_author_id model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_instance_full_clean_with_foreignkey_id model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_modelform_save_with_archived_writer_book model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_modelform_validation_allows_archived_writer_book model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_modelform_validation_writerprofile_allows_archived_writer model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_one_to_one_field_validate_writerprofile
coverage json -o coverage.json
: '>>>>> End Test Output'
