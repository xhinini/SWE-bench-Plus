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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.FakeLHS.__init__ model_fields.test_jsonfield_llm.FakeLHS.preprocess_lhs model_fields.test_jsonfield_llm.FakeLHSParams.__init__ model_fields.test_jsonfield_llm.FakeLHSParams.preprocess_lhs model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_isnull_true_combines_haskey_and_lhs_params_in_correct_order model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_isnull_true_uses_or_and_is_null_and_returns_lhs_params_when_haskey_has_no_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_oracle_true_includes_is_null_literal_in_sql model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_sqlite_isnull_false_uses_is_not_null_template model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_sqlite_isnull_true_uses_is_null_template model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_as_sqlite_never_wraps_with_not
coverage json -o coverage.json
: '>>>>> End Test Output'
