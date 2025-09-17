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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 db_functions.datetime.test_extract_trunc_llm.DummyCompiler.compile db_functions.datetime.test_extract_trunc_llm.DummyConnection.__init__ db_functions.datetime.test_extract_trunc_llm.DummyOps.__init__ db_functions.datetime.test_extract_trunc_llm.DummyOps.datetime_cast_date_sql db_functions.datetime.test_extract_trunc_llm.DummyOps.datetime_cast_time_sql db_functions.datetime.test_extract_trunc_llm.TruncDateTimeNoTZTests.test_truncdate_no_tzinfo_and_use_tz_false db_functions.datetime.test_extract_trunc_llm.TruncDateTimeNoTZTests.test_truncdate_with_tzinfo_ignored_when_use_tz_false db_functions.datetime.test_extract_trunc_llm.TruncDateTimeNoTZTests.test_trunctime_no_tzinfo_and_use_tz_false db_functions.datetime.test_extract_trunc_llm.TruncDateTimeNoTZTests.test_trunctime_with_tzinfo_ignored_when_use_tz_false db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneTests.test_truncdate_uses_current_timezone_when_no_explicit_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneTests.test_truncdate_with_pytz_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneTests.test_truncdate_with_stdlib_fixed_offset_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneTests.test_trunctime_with_pytz_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneTests.test_trunctime_with_stdlib_fixed_offset_tzinfo db_functions.datetime.test_extract_trunc_llm.make_trunc_instance
coverage json -o coverage.json
: '>>>>> End Test Output'
