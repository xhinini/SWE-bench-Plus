#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_timesince_llm.TZAwarePivotTimesinceAdditionalTests.setUp utils_tests.test_timesince_llm.TZAwarePivotTimesinceAdditionalTests.test_month_difference_default_and_fixed_timezone utils_tests.test_timesince_llm.TZAwarePivotTimesinceAdditionalTests.test_month_difference_different_fixed_timezones
coverage json -o coverage.json
: '>>>>> End Test Output'
