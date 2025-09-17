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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.RelatedFieldValidationTests.create_archived_writer model_forms.test_models_llm.RelatedFieldValidationTests.test_book_author_validate_allows_hidden_pk model_forms.test_models_llm.RelatedFieldValidationTests.test_foreignkey_full_clean_allows_hidden_instance model_forms.test_models_llm.RelatedFieldValidationTests.test_foreignkey_validate_allows_hidden_instance_object model_forms.test_models_llm.RelatedFieldValidationTests.test_foreignkey_validate_allows_hidden_pk_direct_call model_forms.test_models_llm.RelatedFieldValidationTests.test_foreignkey_validate_allows_hidden_pk_str model_forms.test_models_llm.RelatedFieldValidationTests.test_foreignkey_validate_rejects_nonexistent_pk model_forms.test_models_llm.RelatedFieldValidationTests.test_foreignkey_validate_with_different_types model_forms.test_models_llm.RelatedFieldValidationTests.test_full_clean_rejects_nonexistent_pk model_forms.test_models_llm.RelatedFieldValidationTests.test_onetoone_validate_allows_hidden_pk model_forms.test_models_llm.RelatedFieldValidationTests.test_validate_uses_base_manager_not_default
coverage json -o coverage.json
: '>>>>> End Test Output'
