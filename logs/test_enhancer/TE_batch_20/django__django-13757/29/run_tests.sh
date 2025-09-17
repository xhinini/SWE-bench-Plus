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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_oracle_handles_integer_key_in_path_for_isnull_true model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_oracle_isnull_true_includes_is_null_and_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_oracle_isnull_true_uses_haskey_params_then_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_oracle_percent_in_key_is_escaped_in_path model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_sqlite_integer_key_path_in_isnull_true model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_sqlite_isnull_true_uses_json_type_is_null_and_params model_fields.test_jsonfield_llm.KeyTransformIsNullSQLTests.test_sqlite_param_ordering_with_mocked_haskey_returns
coverage json -o coverage.json
: '>>>>> End Test Output'
