#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_state_llm.RealAppsInitTests.test_real_apps_dict_assertion_message_empty migrations.test_state_llm.RealAppsInitTests.test_real_apps_frozenset_assertion_message_empty migrations.test_state_llm.RealAppsInitTests.test_real_apps_generator_assertion_message_empty migrations.test_state_llm.RealAppsInitTests.test_real_apps_int_assertion_message_empty migrations.test_state_llm.RealAppsInitTests.test_real_apps_list_assertion_message_empty migrations.test_state_llm.RealAppsInitTests.test_real_apps_string_assertion_message_empty migrations.test_state_llm.RealAppsInitTests.test_real_apps_tuple_assertion_message_empty
coverage json -o coverage.json
: '>>>>> End Test Output'
