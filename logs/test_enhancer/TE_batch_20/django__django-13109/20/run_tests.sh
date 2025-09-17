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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests._create_archived_writer_via_base model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.setUp model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_field_validate_direct_with_writer_id model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_field_validate_direct_with_writer_object model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_full_clean_accepts_none_value model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_full_clean_allows_archived_related_via_base_manager_using_writer_id model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_full_clean_allows_archived_related_via_base_manager_using_writer_object model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_one_to_one_validate_uses_base_manager model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_validate_does_not_call_default_manager_when_monkeypatched_direct model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_validate_does_not_call_default_manager_when_monkeypatched_full_clean model_forms.test_models_llm.ForeignKeyBaseManagerValidationTests.test_validate_raises_for_nonexistent_related
coverage json -o coverage.json
: '>>>>> End Test Output'
