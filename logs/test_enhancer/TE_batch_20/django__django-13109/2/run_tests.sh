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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.setUp model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_one_to_one_validate_allows_archived_with_instance model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_one_to_one_validate_allows_archived_with_pk model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_one_to_one_validate_raises_for_nonexistent model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_allows_archived_with_instance model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_allows_archived_with_pk model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_allows_visible_writer_with_pk model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_raises_for_empty_string model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_raises_for_nonexistent_value model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_returns_on_none model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_uses_base_manager_when_default_manager_filters
coverage json -o coverage.json
: '>>>>> End Test Output'
