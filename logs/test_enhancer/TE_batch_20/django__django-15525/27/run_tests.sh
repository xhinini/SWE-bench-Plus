#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_data_is_mutated_with_added_pk backends.sqlite.test_features_llm.BuildInstanceTests.test_manager_raises_doesnotexist_no_error_pk_remains_none backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_uses_related_field_from_data backends.sqlite.test_features_llm.BuildInstanceTests.test_original_data_preserved_except_pk_addition backends.sqlite.test_features_llm.BuildInstanceTests.test_pk_none_calls_get_by_natural_key_with_db_and_sets_pk backends.sqlite.test_features_llm.BuildInstanceTests.test_pk_to_python_called_on_retrieved_pk backends.sqlite.test_features_llm.make_model_class
coverage json -o coverage.json
: '>>>>> End Test Output'
