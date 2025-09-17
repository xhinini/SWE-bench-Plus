#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_timesince_llm.PivotTZInfoTests.test_aware_exact_years utils_tests.test_timesince_llm.PivotTZInfoTests.test_aware_one_month_one_day utils_tests.test_timesince_llm.PivotTZInfoTests.test_depth_with_aware_pivot utils_tests.test_timesince_llm.PivotTZInfoTests.test_feb29_to_non_leap_year_months_leading_part utils_tests.test_timesince_llm.PivotTZInfoTests.test_reversed_with_aware utils_tests.test_timesince_llm.PivotTZInfoTests.test_timeuntil_aware_exact_years
coverage json -o coverage.json
: '>>>>> End Test Output'
