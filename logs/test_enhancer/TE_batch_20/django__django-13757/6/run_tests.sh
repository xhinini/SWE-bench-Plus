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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.DummyCompiler.compile model_fields.test_jsonfield_llm.DummyConnection.__init__ model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_haskey_sql_with_percent_and_lhs_escape model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_handles_empty_haskey_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_returns_not_or_is_null model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_with_nested_key_transform_concatenates_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_haskey_template_used_once_and_params_returned model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_false_uses_is_not_null_template model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_uses_is_null_template model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_template_passed_through_correctly_for_multiple_calls
coverage json -o coverage.json
: '>>>>> End Test Output'
