#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_timesince_llm.TimesincePivotTZTests.assert_aware_equals_naive utils_tests.test_timesince_llm.TimesincePivotTZTests.setUp utils_tests.test_timesince_llm.TimesincePivotTZTests.test_minute_and_hour_edges_with_tz
coverage json -o coverage.json
: '>>>>> End Test Output'
