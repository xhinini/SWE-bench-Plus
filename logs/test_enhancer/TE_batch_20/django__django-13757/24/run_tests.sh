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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_jsonfield_llm.DummyCompiler.compile model_fields.test_jsonfield_llm.DummyConnection.__init__ model_fields.test_jsonfield_llm.KeyTransformIsNullTests.setUp model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_false_simple_key model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_nested_key model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_numeric_key model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_percent_key model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_oracle_isnull_true_simple_key model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_false_simple_key model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_nested_key model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_numeric_key model_fields.test_jsonfield_llm.KeyTransformIsNullTests.test_sqlite_isnull_true_simple_key
coverage json -o coverage.json
: '>>>>> End Test Output'
