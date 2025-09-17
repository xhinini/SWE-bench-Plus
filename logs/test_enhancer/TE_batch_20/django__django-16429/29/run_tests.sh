#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_timesince_llm.TzPivotRegressionTests.test_aware_different_timezone_offsets utils_tests.test_timesince_llm.TzPivotRegressionTests.test_aware_month_and_weeks utils_tests.test_timesince_llm.TzPivotRegressionTests.test_aware_month_exact utils_tests.test_timesince_llm.TzPivotRegressionTests.test_aware_year_exact utils_tests.test_timesince_llm.TzPivotRegressionTests.test_depth_handling_with_aware utils_tests.test_timesince_llm.TzPivotRegressionTests.test_pivot_day_rollover_no_exception utils_tests.test_timesince_llm.TzPivotRegressionTests.test_timeuntil_aware_month utils_tests.test_timesince_llm.TzPivotRegressionTests.test_timeuntil_years_and_months_aware utils_tests.test_timesince_llm.TzPivotRegressionTests.test_years_and_months_with_aware_datetimes
coverage json -o coverage.json
: '>>>>> End Test Output'
