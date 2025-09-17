#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_timesince_llm.PivotTZInfoTests.test_aware_months_pivot_nonzero utils_tests.test_timesince_llm.PivotTZInfoTests.test_aware_years_pivot_nonzero utils_tests.test_timesince_llm.PivotTZInfoTests.test_timesince_aware_future_returns_zero utils_tests.test_timesince_llm.PivotTZInfoTests.test_timeuntil_aware_months_pivot_nonzero utils_tests.test_timesince_llm.PivotTZInfoTests.test_timeuntil_aware_past_returns_zero utils_tests.test_timesince_llm.PivotTZInfoTests.test_timeuntil_aware_with_years_and_months
coverage json -o coverage.json
: '>>>>> End Test Output'
