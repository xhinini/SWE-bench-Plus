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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.DummyCompiler.compile model_fields.test_jsonfield_llm.DummyConnection.__init__ model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_oracle_and_sqlite_behavior_difference_detects_candidate_bug model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_oracle_isnull_false_returns_has_key_sql model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_oracle_isnull_true_nested_keytransform_returns_or_with_is_null model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_oracle_isnull_true_returns_or_expression_with_is_null model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_oracle_isnull_true_with_rawsql_previous_inlines_path model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_sqlite_isnull_false_returns_json_type_is_not_null model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_sqlite_isnull_true_nested_returns_is_null_and_param_path_contains_compiled model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_sqlite_isnull_true_returns_json_type_is_null_and_params
coverage json -o coverage.json
: '>>>>> End Test Output'
