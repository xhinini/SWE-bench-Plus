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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.DummyCompiler.compile model_fields.test_jsonfield_llm.DummyConnection.__init__ model_fields.test_jsonfield_llm.FakeKeyTransform.__init__ model_fields.test_jsonfield_llm.KeyTransformIsNullTests.setUp model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_isnull_false_uses_haskey model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_isnull_true_combines_haskey_and_is_null model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_sqlite_isnull_false_uses_haskey_sql_with_is_not_null_template model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_sqlite_isnull_true_uses_haskey_sql_with_is_null_template model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_integration_with_haskey_on_rawsql_lhs_oracle model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_combination_params_include_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_haskey_called_once_and_not_negated model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_haskey_not_simple_negation model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_templates_use_compile_json_path
coverage json -o coverage.json
: '>>>>> End Test Output'
