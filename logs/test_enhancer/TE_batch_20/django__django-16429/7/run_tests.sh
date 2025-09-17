#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.setUp utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.test_aware_one_month_different_timezones utils_tests.test_timesince_llm.TZAwarePivotTimesinceTests.test_aware_six_months_crossing_year_boundary
coverage json -o coverage.json
: '>>>>> End Test Output'
