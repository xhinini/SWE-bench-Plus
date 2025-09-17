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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.KeyTransformIsNullTests._make_lhs model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_combines_sql_and_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_param_order model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_with_no_haskey_params_returns_lhs_params_only model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_with_no_params_at_all model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_does_not_negate_sql_and_preserves_params model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_uses_is_null_template_and_returns_unmodified_sql
coverage json -o coverage.json
: '>>>>> End Test Output'
