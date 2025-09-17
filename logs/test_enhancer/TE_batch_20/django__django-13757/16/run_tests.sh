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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.DummyCompiler.__init__ model_fields.test_jsonfield_llm.DummyCompiler.compile model_fields.test_jsonfield_llm.DummyConnection.__init__ model_fields.test_jsonfield_llm.DummyFeatures.__init__ model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_false_returns_json_exists_and_no_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_false_returns_no_params_even_if_compiler_has_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_nested_key_transform_includes_json_exists_and_is_null model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_returns_lhs_params_even_with_multiple_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_returns_not_or_is_null_and_lhs_params_appended model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_false_uses_is_not_null_and_params_order model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_uses_is_null_and_params_order model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_with_integer_key_uses_bracket_path model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_template_includes_json_type_for_both_true_and_false
coverage json -o coverage.json
: '>>>>> End Test Output'
