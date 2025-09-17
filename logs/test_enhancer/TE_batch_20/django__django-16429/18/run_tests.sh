#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_timesince_llm.TZAwarePivotExtraTests.test_aware_depth_years_months utils_tests.test_timesince_llm.TZAwarePivotExtraTests.test_aware_different_timezones_month utils_tests.test_timesince_llm.TZAwarePivotExtraTests.test_aware_large_years utils_tests.test_timesince_llm.TZAwarePivotExtraTests.test_aware_month_day_edge_same_tz utils_tests.test_timesince_llm.TZAwarePivotExtraTests.test_aware_months_same_tz utils_tests.test_timesince_llm.TZAwarePivotExtraTests.test_aware_pivot_with_custom_fixed_timezone utils_tests.test_timesince_llm.TZAwarePivotExtraTests.test_aware_time_component_affects_months utils_tests.test_timesince_llm.TZAwarePivotExtraTests.test_aware_years_months_same_tz utils_tests.test_timesince_llm.TZAwarePivotExtraTests.test_aware_years_same_tz utils_tests.test_timesince_llm.TZAwarePivotExtraTests.test_timeuntil_aware_months
coverage json -o coverage.json
: '>>>>> End Test Output'
