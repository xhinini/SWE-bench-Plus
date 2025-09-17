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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_isnull_false_returns_haskey_sql model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_isnull_true_includes_is_null_and_not model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_isnull_true_with_compiled_lhs_params_returns_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_isnull_true_with_integer_key_on_lhs model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_isnull_true_with_nested_key_contains_array_index model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_isnull_true_with_percent_in_key_escapes_formatting model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_sqlite_isnull_false_contains_is_not_null model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_sqlite_isnull_true_contains_json_type_and_is_null model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_sqlite_isnull_true_with_compiler_params_returns_params_include_path model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_sqlite_isnull_true_with_nested_key_contains_array_index model_fields.test_jsonfield_llm._CompilerStub.__init__ model_fields.test_jsonfield_llm._CompilerStub.compile model_fields.test_jsonfield_llm._ConnectionStub.__init__
coverage json -o coverage.json
: '>>>>> End Test Output'
