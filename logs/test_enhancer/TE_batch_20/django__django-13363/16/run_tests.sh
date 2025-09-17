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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 db_functions.datetime.test_extract_trunc_llm._make_aware db_functions.datetime.test_extract_trunc_llm.test_truncdate_none_returns_none_with_explicit_tzinfo db_functions.datetime.test_extract_trunc_llm.test_truncdate_respects_explicit_tzinfo db_functions.datetime.test_extract_trunc_llm.test_truncdate_tzinfo_precedence_over_current_timezone db_functions.datetime.test_extract_trunc_llm.test_truncdate_with_fixed_offset_tzinfo db_functions.datetime.test_extract_trunc_llm.test_truncdate_with_named_tz_and_override_different_current db_functions.datetime.test_extract_trunc_llm.test_trunctime_none_returns_none_with_explicit_tzinfo db_functions.datetime.test_extract_trunc_llm.test_trunctime_respects_explicit_tzinfo db_functions.datetime.test_extract_trunc_llm.test_trunctime_tzinfo_precedence_over_current_timezone db_functions.datetime.test_extract_trunc_llm.test_trunctime_with_fixed_offset_tzinfo db_functions.datetime.test_extract_trunc_llm.test_trunctime_with_named_tz_and_override_different_current
coverage json -o coverage.json
: '>>>>> End Test Output'
