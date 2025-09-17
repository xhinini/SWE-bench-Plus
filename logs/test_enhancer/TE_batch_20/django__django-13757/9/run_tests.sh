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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.DummyCompiler.__init__ model_fields.test_jsonfield_llm.DummyCompiler.compile model_fields.test_jsonfield_llm.DummyConnection.__init__ model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_oracle_isnull_false_returns_has_key_sql model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_oracle_isnull_true_includes_not_has_key_or_is_null model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_oracle_nested_key_transform_isnull_true model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_oracle_percent_in_key_escapes_formatting model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_oracle_preserves_lhs_params_for_isnull_true model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_sqlite_isnull_false_uses_json_type_is_not_null model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_sqlite_isnull_true_uses_json_type_is_null model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_sqlite_numeric_index_key_uses_bracket_path_true model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_as_sqlite_preserves_lhs_params
coverage json -o coverage.json
: '>>>>> End Test Output'
