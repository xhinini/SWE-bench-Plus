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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.DummyCompiler.__init__ model_fields.test_jsonfield_llm.DummyCompiler.compile model_fields.test_jsonfield_llm.DummyConnection.__init__ model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_false_returns_has_key_sql_and_no_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_includes_or_and_is_null_and_returns_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_no_missing_lhs_params_on_chain_of_transforms model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_param_is_lhs_param_when_rhs_is_keytransform model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_with_nested_keytransform_returns_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_with_numeric_key_returns_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_with_percent_character_in_key_escapes_and_returns_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_false_uses_is_not_null_template model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_uses_is_null_template_and_returns_path_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_with_multiple_rhs_keys_returns_multiple_path_params
coverage json -o coverage.json
: '>>>>> End Test Output'
