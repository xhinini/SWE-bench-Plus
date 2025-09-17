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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 db_functions.datetime.test_extract_trunc_llm.DummyCompiler.compile db_functions.datetime.test_extract_trunc_llm.DummyConnection.__init__ db_functions.datetime.test_extract_trunc_llm.DummyLHS.__init__ db_functions.datetime.test_extract_trunc_llm.RecordingOps.__init__ db_functions.datetime.test_extract_trunc_llm.RecordingOps.datetime_cast_date_sql db_functions.datetime.test_extract_trunc_llm.RecordingOps.datetime_cast_time_sql db_functions.datetime.test_extract_trunc_llm.TruncSQLNoUseTZTests.test_truncdate_when_USETZ_false_ignores_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncSQLNoUseTZTests.test_truncdate_with_fixed_offset_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncSQLNoUseTZTests.test_trunctime_when_USETZ_false_ignores_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncSQLNoUseTZTests.test_trunctime_with_different_lhs_output_field_types db_functions.datetime.test_extract_trunc_llm.TruncSQLTimezoneTests.test_truncdate_explicit_tzinfo_takes_precedence_over_override db_functions.datetime.test_extract_trunc_llm.TruncSQLTimezoneTests.test_truncdate_uses_current_timezone_when_no_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncSQLTimezoneTests.test_truncdate_uses_explicit_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncSQLTimezoneTests.test_trunctime_explicit_tzinfo_takes_precedence_over_override db_functions.datetime.test_extract_trunc_llm.TruncSQLTimezoneTests.test_trunctime_uses_current_timezone_when_no_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncSQLTimezoneTests.test_trunctime_uses_explicit_tzinfo
coverage json -o coverage.json
: '>>>>> End Test Output'
