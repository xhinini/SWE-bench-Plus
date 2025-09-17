#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_state_llm.RealAppsInitTests.test_real_apps_empty_list_raises_empty_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_empty_tuple_raises_empty_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_frozenset_raises_empty_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_generator_raises_empty_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_iterator_raises_empty_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_list_raises_empty_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_map_raises_empty_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_range_raises_empty_message migrations.test_state_llm.RealAppsInitTests.test_real_apps_tuple_raises_empty_message
coverage json -o coverage.json
: '>>>>> End Test Output'
