#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_state_llm.RealAppsAssertionMessageTests.test_dict_raises_assertion_no_message migrations.test_state_llm.RealAppsAssertionMessageTests.test_empty_list_raises_assertion_no_message migrations.test_state_llm.RealAppsAssertionMessageTests.test_frozenset_raises_assertion_no_message migrations.test_state_llm.RealAppsAssertionMessageTests.test_generator_raises_assertion_no_message migrations.test_state_llm.RealAppsAssertionMessageTests.test_list_raises_assertion_no_message migrations.test_state_llm.RealAppsAssertionMessageTests.test_map_iterator_raises_assertion_no_message migrations.test_state_llm.RealAppsAssertionMessageTests.test_string_raises_assertion_no_message migrations.test_state_llm.RealAppsAssertionMessageTests.test_tuple_raises_assertion_no_message
coverage json -o coverage.json
: '>>>>> End Test Output'
