#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_state_llm.RealAppsInitTests.test_real_apps_rejects_empty_list_without_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_rejects_empty_tuple_without_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_rejects_frozenset_without_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_rejects_generator_without_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_rejects_list_without_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_rejects_range_without_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_rejects_string_without_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_rejects_tuple_without_message
coverage json -o coverage.json
: '>>>>> End Test Output'
