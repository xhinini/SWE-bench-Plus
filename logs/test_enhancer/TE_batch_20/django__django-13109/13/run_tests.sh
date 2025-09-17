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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_base_manager_filter_is_used_during_validate model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_default_manager_filter_not_called_during_validate model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_multiple_related_fields_do_not_interfere model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_parent_link_skips_validation model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_accepts_object_visible_only_via_base_manager_article model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_accepts_object_visible_only_via_base_manager_book model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_none_value_does_not_raise model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_raises_when_object_missing model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_with_string_value_for_to_field model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_with_to_field_on_self_relation
coverage json -o coverage.json
: '>>>>> End Test Output'
