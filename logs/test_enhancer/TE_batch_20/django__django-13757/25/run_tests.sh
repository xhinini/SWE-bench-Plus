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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.DummyKeyTransform.__init__ model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_oracle_isnull_true_both_no_params_returns_no_params model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_oracle_isnull_true_haskey_no_params_uses_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_oracle_isnull_true_includes_haskey_and_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_sqlite_isnull_true_passthrough_params_and_sql model_fields.test_jsonfield_llm.KeyTransformIsNullRegressionTests.test_sqlite_isnull_true_uses_is_null_template
coverage json -o coverage.json
: '>>>>> End Test Output'
