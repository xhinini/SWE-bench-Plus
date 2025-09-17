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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.DummyKeyTransform.__init__ model_fields.test_jsonfield_llm.DummyKeyTransform.preprocess_lhs model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_appends_multiple_lhs_params_in_order model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_combines_not_haskey_or_lhs_is_null_and_appends_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_includes_lhs_sql_text_in_condition model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_with_no_lhs_params_just_returns_haskey_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_false_passes_through_parameters model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_returns_haskey_result_not_negated model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_uses_json_type_is_null_template
coverage json -o coverage.json
: '>>>>> End Test Output'
