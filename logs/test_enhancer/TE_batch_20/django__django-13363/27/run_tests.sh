#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTZNameTests.test_truncdate_explicit_tzinfo_takes_priority_over_current_timezone db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTZNameTests.test_truncdate_returns_sql_and_params db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTZNameTests.test_truncdate_uses_current_timezone_when_no_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTZNameTests.test_truncdate_uses_explicit_tzinfo_for_tzname db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTZNameTests.test_truncdate_with_none_tzname_when_USE_TZ_false_and_no_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTZNameTests.test_truncdate_with_utc_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTZNameTests.test_trunctime_returns_sql_and_params db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTZNameTests.test_trunctime_uses_current_timezone_when_no_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTZNameTests.test_trunctime_uses_explicit_tzinfo_for_tzname db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTZNameTests.test_trunctime_with_USE_TZ_false_ignores_tzinfo
coverage json -o coverage.json
: '>>>>> End Test Output'
