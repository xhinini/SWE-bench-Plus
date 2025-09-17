#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.make_model_with_mapping backends.sqlite.test_features_llm.BuildInstanceTests.test_calls_to_python_on_pk_conversion backends.sqlite.test_features_llm.BuildInstanceTests.test_complex_natural_key_with_db_component backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_attribute_error_propagates backends.sqlite.test_features_llm.BuildInstanceTests.test_non_string_db_value_is_used backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_pk_from_natural_key_for_default_db backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_pk_from_natural_key_for_other_db
coverage json -o coverage.json
: '>>>>> End Test Output'
