#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.sqlite.test_features_llm.BuildInstanceTests.test_build_instance_mutates_data_with_converted_pk backends.sqlite.test_features_llm.BuildInstanceTests.test_calls_db_manager_with_provided_db backends.sqlite.test_features_llm.BuildInstanceTests.test_get_by_natural_key_raises_doesnotexist_is_handled backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_accessing_state_db_without_setting_would_fail_but_build_instance_sets_it backends.sqlite.test_features_llm.BuildInstanceTests.test_natural_key_with_multiple_values_passed_to_get_by_natural_key backends.sqlite.test_features_llm.BuildInstanceTests.test_pk_missing_with_natural_key_uses_db_and_sets_pk backends.sqlite.test_features_llm.BuildInstanceTests.test_to_python_called_on_pk backends.sqlite.test_features_llm.make_fake_model
coverage json -o coverage.json
: '>>>>> End Test Output'
