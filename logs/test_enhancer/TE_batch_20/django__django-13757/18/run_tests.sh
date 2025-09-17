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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_handles_empty_haskey_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_isnull_true_combines_haskey_and_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_isnull_true_concatenates_multiple_params_in_order model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_preprocess_lhs_called_when_isnull_true model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_sqlite_calls_haskey_as_sql_once_and_returns_value model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_sqlite_uses_json_type_is_not_null_template_for_false model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_sqlite_uses_json_type_is_null_template
coverage json -o coverage.json
: '>>>>> End Test Output'
