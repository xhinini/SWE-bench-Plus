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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests._make_article_instance model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.setUp model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_full_clean_allows_archived_writer model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_full_clean_raises_for_nonexistent_id model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_modelform_default_queryset_rejects_archived_writer model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_modelform_with_base_manager_queryset_accepts_archived_writer model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_accepts_string_pk model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_raises_for_nonexistent_id model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_with_archived_writer_id_does_not_raise model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_with_archived_writer_instance_does_not_raise model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_writer_default_manager_filters_but_base_manager_includes
coverage json -o coverage.json
: '>>>>> End Test Output'
