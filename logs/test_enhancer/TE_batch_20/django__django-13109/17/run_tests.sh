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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.setUp model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_parent_link_one_to_one_early_return model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_allows_instance_hidden_by_default_manager model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_allows_pk_hidden_by_default_manager model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_none_value_no_error model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_raises_for_nonexistent_pk model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_to_field_non_pk_missing_raises model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_uses_base_manager_not_default_manager_explicit_assertion model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_with_limit_choices_to_callable_accepts model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_with_limit_choices_to_dict_rejects model_forms.test_models_llm.ForeignKeyValidateBaseManagerTests.test_validate_with_limit_choices_to_q_rejects
coverage json -o coverage.json
: '>>>>> End Test Output'
