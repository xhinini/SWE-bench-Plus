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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 db_functions.datetime.test_extract_trunc_llm.TruncDateTimeExplicitTZTests.test_trunc_date_explicit_tz_priority_with_override db_functions.datetime.test_extract_trunc_llm.TruncDateTimeExplicitTZTests.test_trunc_date_explicit_tz_without_override db_functions.datetime.test_extract_trunc_llm.TruncDateTimeExplicitTZTests.test_trunc_date_falls_back_to_current_timezone_when_no_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeExplicitTZTests.test_trunc_date_none_with_tzinfo_returns_none db_functions.datetime.test_extract_trunc_llm.TruncDateTimeExplicitTZTests.test_trunc_date_with_fixed_offset_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeExplicitTZTests.test_trunc_time_explicit_tz_priority_with_override db_functions.datetime.test_extract_trunc_llm.TruncDateTimeExplicitTZTests.test_trunc_time_explicit_tz_without_override db_functions.datetime.test_extract_trunc_llm.TruncDateTimeExplicitTZTests.test_trunc_time_falls_back_to_current_timezone_when_no_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeExplicitTZTests.test_trunc_time_none_with_tzinfo_returns_none db_functions.datetime.test_extract_trunc_llm.TruncDateTimeExplicitTZTests.test_trunc_time_with_fixed_offset_tzinfo
coverage json -o coverage.json
: '>>>>> End Test Output'
