#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_timesince_llm.TimesinceTZInfoRegressionTests.test_aware_timesince_different_timezones utils_tests.test_timesince_llm.TimesinceTZInfoRegressionTests.test_aware_timesince_month_wrap_exact utils_tests.test_timesince_llm.TimesinceTZInfoRegressionTests.test_aware_timesince_no_exception_on_pivot_construction utils_tests.test_timesince_llm.TimesinceTZInfoRegressionTests.test_aware_timesince_one_year_one_month_exact utils_tests.test_timesince_llm.TimesinceTZInfoRegressionTests.test_aware_timeuntil_one_year_one_month_exact utils_tests.test_timesince_llm.TimesinceTZInfoRegressionTests.test_timeuntil_no_exception_on_pivot_construction utils_tests.test_timesince_llm.TimesinceTZInfoRegressionTests.test_timeuntil_with_different_timezones
coverage json -o coverage.json
: '>>>>> End Test Output'
