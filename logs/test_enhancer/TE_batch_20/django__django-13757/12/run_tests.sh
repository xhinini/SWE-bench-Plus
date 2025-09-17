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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.DummyCompiler.__init__ model_fields.test_jsonfield_llm.DummyCompiler.compile model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_false_returns_has_key_sql_without_is_null model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_combined_logic_format model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_includes_is_null_and_has_key_expr model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_lhs_present_in_sql model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_propagates_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_nested_key_transform_isnull_true_contains_is_null model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_false_uses_json_type_is_not_null model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_uses_json_type_is_null model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_with_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_nested_key_transform_isnull_true_contains_is_null
coverage json -o coverage.json
: '>>>>> End Test Output'
