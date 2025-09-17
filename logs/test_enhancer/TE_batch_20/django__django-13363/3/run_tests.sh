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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 db_functions.datetime.test_extract_trunc_llm._DummyExpr.__init__ db_functions.datetime.test_extract_trunc_llm._make_dummy_connection db_functions.datetime.test_extract_trunc_llm.test_truncdate_as_sql_returns_sql_and_params db_functions.datetime.test_extract_trunc_llm.test_truncdate_honors_pytz_utc db_functions.datetime.test_extract_trunc_llm.test_truncdate_ignores_tz_when_USE_TZ_false db_functions.datetime.test_extract_trunc_llm.test_truncdate_uses_current_timezone_when_no_explicit_tz db_functions.datetime.test_extract_trunc_llm.test_truncdate_uses_explicit_tzinfo_over_current_timezone db_functions.datetime.test_extract_trunc_llm.test_truncdate_with_fixed_offset_tzinfo db_functions.datetime.test_extract_trunc_llm.test_trunctime_ignores_tz_when_USE_TZ_false db_functions.datetime.test_extract_trunc_llm.test_trunctime_uses_current_timezone_when_no_explicit_tz db_functions.datetime.test_extract_trunc_llm.test_trunctime_uses_explicit_tzinfo_over_current_timezone
coverage json -o coverage.json
: '>>>>> End Test Output'
