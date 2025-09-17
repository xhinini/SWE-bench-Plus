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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateTests._make_article_instance model_forms.test_models_llm.ForeignKeyValidateTests.setUp model_forms.test_models_llm.ForeignKeyValidateTests.test_field_validate_allows_archived_writer model_forms.test_models_llm.ForeignKeyValidateTests.test_full_clean_with_writer_id_allows_archived_writer model_forms.test_models_llm.ForeignKeyValidateTests.test_full_clean_with_writer_object_allows_archived_writer model_forms.test_models_llm.ForeignKeyValidateTests.test_limit_choices_to_is_respected_after_using_base_manager model_forms.test_models_llm.ForeignKeyValidateTests.test_one_to_one_field_validate_allows_archived_writer model_forms.test_models_llm.ForeignKeyValidateTests.test_one_to_one_full_clean_with_writer_id_allows_archived_writer model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_none_value_returns_without_error model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_raises_when_object_does_not_exist model_forms.test_models_llm.ForeignKeyValidateTests.test_validate_with_to_field_on_self_referential_fk
coverage json -o coverage.json
: '>>>>> End Test Output'
