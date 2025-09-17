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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.RelatedFieldBaseManagerTests.create_archived_writer model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_clean_fields_uses_base_manager model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_foreignkey_validate_allows_archived_target model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_foreignkey_validate_does_not_use_default_manager_filter model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_foreignkey_validate_does_not_use_default_manager_get_queryset model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_one_to_one_full_clean_allows_archived_target model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_one_to_one_validate_allows_archived_target model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_one_to_one_validate_does_not_use_default_manager_get_queryset model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_validate_does_not_use_default_manager_even_if_default_filter_raises model_forms.test_models_llm.RelatedFieldBaseManagerTests.test_validate_raises_for_nonexistent_pk
coverage json -o coverage.json
: '>>>>> End Test Output'
