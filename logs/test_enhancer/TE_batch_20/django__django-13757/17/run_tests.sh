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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.DummyCompiler.compile model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests._oracle_connection model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests._sqlite_connection model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.setUp model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_oracle_isnull_false_matches_haskey model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_oracle_isnull_false_with_numeric_key model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_oracle_isnull_true_composite_sql_and_params model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_oracle_isnull_true_escapes_percent_in_key_name model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_oracle_isnull_true_params_includes_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_oracle_isnull_true_with_nested_keytransform model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_sqlite_isnull_false_uses_not_null_template model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_sqlite_isnull_true_uses_null_template model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_sqlite_isnull_true_with_nested_keytransform
coverage json -o coverage.json
: '>>>>> End Test Output'
