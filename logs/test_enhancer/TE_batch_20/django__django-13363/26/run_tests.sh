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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 db_functions.datetime.test_extract_trunc_llm.test_truncdate_dst_transition_explicit_tz_respected db_functions.datetime.test_extract_trunc_llm.test_truncdate_explicit_tz_overrides_current db_functions.datetime.test_extract_trunc_llm.test_truncdate_explicit_tz_overrides_timezone_override db_functions.datetime.test_extract_trunc_llm.test_truncdate_none_uses_current_timezone db_functions.datetime.test_extract_trunc_llm.test_truncdate_utc_tzinfo_overrides_current db_functions.datetime.test_extract_trunc_llm.test_trunctime_dst_transition_explicit_tz_respected db_functions.datetime.test_extract_trunc_llm.test_trunctime_explicit_tz_overrides_current db_functions.datetime.test_extract_trunc_llm.test_trunctime_explicit_tz_overrides_timezone_override db_functions.datetime.test_extract_trunc_llm.test_trunctime_none_uses_current_timezone db_functions.datetime.test_extract_trunc_llm.test_trunctime_utc_tzinfo_overrides_current
coverage json -o coverage.json
: '>>>>> End Test Output'
