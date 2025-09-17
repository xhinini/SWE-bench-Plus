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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.RelatedFieldValidateTests.setUp model_forms.test_models_llm.RelatedFieldValidateTests.test_base_manager_includes_archived_writer model_forms.test_models_llm.RelatedFieldValidateTests.test_default_manager_excludes_archived_writer model_forms.test_models_llm.RelatedFieldValidateTests.test_fk_validate_accepts_archived_writer_by_instance model_forms.test_models_llm.RelatedFieldValidateTests.test_fk_validate_accepts_archived_writer_by_pk model_forms.test_models_llm.RelatedFieldValidateTests.test_fk_validate_raises_for_nonexistent_value model_forms.test_models_llm.RelatedFieldValidateTests.test_one_to_one_validate_accepts_archived_writer_by_instance model_forms.test_models_llm.RelatedFieldValidateTests.test_one_to_one_validate_accepts_archived_writer_by_pk model_forms.test_models_llm.RelatedFieldValidateTests.test_parent_link_one_to_one_skips_validation model_forms.test_models_llm.RelatedFieldValidateTests.test_validate_none_is_allowed model_forms.test_models_llm.RelatedFieldValidateTests.test_validate_works_when_value_is_string_pk
coverage json -o coverage.json
: '>>>>> End Test Output'
