#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_leaves_pk_none_when_get_by_natural_key_raises backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_with_multiple_arguments backends.sqlite.test_features_llm.BuildInstanceTests.test_preserves_other_fields backends.sqlite.test_features_llm.BuildInstanceTests.test_relation_field_needed_by_natural_key backends.sqlite.test_features_llm.BuildInstanceTests.test_respects_existing_pk_and_does_not_call_manager backends.sqlite.test_features_llm.BuildInstanceTests.test_sets_pk_using_natural_key_and_db_state backends.sqlite.test_features_llm.BuildInstanceTests.test_skips_if_default_manager_has_no_get_by_natural_key backends.sqlite.test_features_llm.BuildInstanceTests.test_skips_natural_key_if_model_has_no_natural_key_attr backends.sqlite.test_features_llm.BuildInstanceTests.test_to_python_conversion_called_on_returned_pk
coverage json -o coverage.json
: '>>>>> End Test Output'
