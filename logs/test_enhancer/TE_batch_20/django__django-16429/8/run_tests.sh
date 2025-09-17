#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_timesince_llm.TZAwarePivotTests.setUp utils_tests.test_timesince_llm.TZAwarePivotTests.test_aware_different_timezones_one_month utils_tests.test_timesince_llm.TZAwarePivotTests.test_aware_exact_one_month utils_tests.test_timesince_llm.TZAwarePivotTests.test_aware_one_year_one_month utils_tests.test_timesince_llm.TZAwarePivotTests.test_end_of_month_pivot_preserves_tz utils_tests.test_timesince_llm.TZAwarePivotTests.test_pivot_includes_hours_when_depth_allows utils_tests.test_timesince_llm.TZAwarePivotTests.test_timesince_depth_with_aware utils_tests.test_timesince_llm.TZAwarePivotTests.test_timesince_explicit_reversed_with_aware utils_tests.test_timesince_llm.TZAwarePivotTests.test_timeuntil_with_aware_datetimes utils_tests.test_timesince_llm.TZAwarePivotTests.test_timeuntil_with_aware_different_timezones utils_tests.test_timesince_llm.TZAwarePivotTests.test_timeuntil_year_and_month_across_timezones
coverage json -o coverage.json
: '>>>>> End Test Output'
