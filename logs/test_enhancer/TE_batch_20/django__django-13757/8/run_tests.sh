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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.DummyCompiler.__init__ model_fields.test_jsonfield_llm.DummyCompiler.compile model_fields.test_jsonfield_llm.DummyConnection.__init__ model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_oracle_isnull_false_params_empty model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_oracle_isnull_false_returns_haskey_sql model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_oracle_isnull_true_includes_is_null_and_or_logic model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_oracle_isnull_true_params_include_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_sqlite_isnull_false_params_include_json_path model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_sqlite_isnull_false_uses_is_not_null_template model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_sqlite_isnull_true_params_include_json_path model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_sqlite_isnull_true_uses_is_null_template model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_oracle_nested_keytransform_isnull_true_includes_is_null
coverage json -o coverage.json
: '>>>>> End Test Output'
