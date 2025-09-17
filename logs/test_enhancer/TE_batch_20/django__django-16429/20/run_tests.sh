#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_timesince_llm.TZAwarePivotMonthsTests._assert_timesince utils_tests.test_timesince_llm.TZAwarePivotMonthsTests.setUp utils_tests.test_timesince_llm.TZAwarePivotMonthsTests.test_aware_month_apr_1 utils_tests.test_timesince_llm.TZAwarePivotMonthsTests.test_aware_month_aug_1 utils_tests.test_timesince_llm.TZAwarePivotMonthsTests.test_aware_month_feb_1 utils_tests.test_timesince_llm.TZAwarePivotMonthsTests.test_aware_month_feb_28 utils_tests.test_timesince_llm.TZAwarePivotMonthsTests.test_aware_month_jul_1 utils_tests.test_timesince_llm.TZAwarePivotMonthsTests.test_aware_month_jun_1 utils_tests.test_timesince_llm.TZAwarePivotMonthsTests.test_aware_month_mar_1 utils_tests.test_timesince_llm.TZAwarePivotMonthsTests.test_aware_month_mar_31 utils_tests.test_timesince_llm.TZAwarePivotMonthsTests.test_aware_month_may_1 utils_tests.test_timesince_llm.TZAwarePivotMonthsTests.test_aware_thousand_years_ago
coverage json -o coverage.json
: '>>>>> End Test Output'
