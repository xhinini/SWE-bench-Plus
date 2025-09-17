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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 db_functions.datetime.test_extract_trunc_llm._patch_and_capture db_functions.datetime.test_extract_trunc_llm.create_aware db_functions.datetime.test_extract_trunc_llm.create_naive_dt db_functions.datetime.test_extract_trunc_llm.test_truncdate_no_use_tz_passes_none db_functions.datetime.test_extract_trunc_llm.test_truncdate_uses_current_tz_when_no_tzinfo db_functions.datetime.test_extract_trunc_llm.test_truncdate_uses_explicit_tz_patch db_functions.datetime.test_extract_trunc_llm.test_truncdate_value_with_explicit_tz db_functions.datetime.test_extract_trunc_llm.test_trunctime_no_use_tz_passes_none db_functions.datetime.test_extract_trunc_llm.test_trunctime_uses_current_tz_when_no_tzinfo db_functions.datetime.test_extract_trunc_llm.test_trunctime_uses_explicit_tz_patch db_functions.datetime.test_extract_trunc_llm.test_trunctime_value_with_explicit_tz
coverage json -o coverage.json
: '>>>>> End Test Output'
