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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_as_oracle_isnull_true_param_concatenation_multiple_params model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_as_oracle_isnull_true_returns_not_or_haskey_or_lhs_is_null model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_as_oracle_isnull_true_with_empty_haskey_params_includes_lhs_params model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_as_oracle_isnull_true_with_no_params_returns_empty_tuple model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_as_sqlite_isnull_true_passes_is_null_template_to_haskey model_fields.test_jsonfield_llm.KeyTransformIsNullLookupTests.test_as_sqlite_returns_haskey_as_sql_result_directly
coverage json -o coverage.json
: '>>>>> End Test Output'
