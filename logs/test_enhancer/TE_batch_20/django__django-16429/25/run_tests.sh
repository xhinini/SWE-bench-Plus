#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.test_aware_different_timezones utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.test_aware_months_rollover utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.test_aware_year_and_month utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.test_days_and_hours_aware utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.test_decrement_month_when_day_greater_aware utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.test_large_years_aware utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.test_minutes_only_aware utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.test_pivot_tzinfo_preserved_prevents_typeerror utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.test_timeuntil_with_aware_datetimes utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.test_weeks_and_days_aware
coverage json -o coverage.json
: '>>>>> End Test Output'
