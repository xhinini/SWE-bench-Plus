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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 db_functions.datetime.test_extract_trunc_llm.DummyOps.__init__ db_functions.datetime.test_extract_trunc_llm.DummyOps.datetime_cast_date_sql db_functions.datetime.test_extract_trunc_llm.DummyOps.datetime_cast_time_sql db_functions.datetime.test_extract_trunc_llm.TruncTZNameTests._compile_and_call_truncdate db_functions.datetime.test_extract_trunc_llm.TruncTZNameTests._compile_and_call_trunctime db_functions.datetime.test_extract_trunc_llm.TruncTZNameTests.test_truncdate_returns_none_when_use_tz_false_even_with_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncTZNameTests.test_truncdate_uses_current_timezone_when_no_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncTZNameTests.test_truncdate_uses_explicit_tzinfo_when_use_tz_true db_functions.datetime.test_extract_trunc_llm.TruncTZNameTests.test_trunctime_returns_none_when_use_tz_false_even_with_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncTZNameTests.test_trunctime_uses_current_timezone_when_no_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncTZNameTests.test_trunctime_uses_explicit_tzinfo_when_use_tz_true
coverage json -o coverage.json
: '>>>>> End Test Output'
