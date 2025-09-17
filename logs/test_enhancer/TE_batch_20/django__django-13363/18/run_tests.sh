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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTznameTests._make_compiler_and_connection db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTznameTests.test_truncdate_accepts_fixed_offset_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTznameTests.test_truncdate_ignores_tzinfo_when_use_tz_false db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTznameTests.test_truncdate_prefers_explicit_tz_over_current_timezone db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTznameTests.test_truncdate_subquery_like_compilation_uses_explicit_tz db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTznameTests.test_truncdate_without_explicit_tz_uses_current_timezone db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTznameTests.test_trunctime_accepts_fixed_offset_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTznameTests.test_trunctime_ignores_tzinfo_when_use_tz_false db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTznameTests.test_trunctime_prefers_explicit_tz_over_current_timezone db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTznameTests.test_trunctime_subquery_like_compilation_uses_explicit_tz db_functions.datetime.test_extract_trunc_llm.TruncDateTimeTznameTests.test_trunctime_without_explicit_tz_uses_current_timezone
coverage json -o coverage.json
: '>>>>> End Test Output'
