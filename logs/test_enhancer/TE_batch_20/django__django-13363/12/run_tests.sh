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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 db_functions.datetime.test_extract_trunc_llm.TruncDateTimeNoTZRegressionTests.test_truncdate_ignores_tzinfo_when_use_tz_false db_functions.datetime.test_extract_trunc_llm.TruncDateTimeNoTZRegressionTests.test_trunctime_ignores_tzinfo_when_use_tz_false db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneRegressionTests.create_model_aware db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneRegressionTests.test_truncdate_respects_explicit_tzinfo_over_current db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneRegressionTests.test_truncdate_subquery_with_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneRegressionTests.test_truncdate_uses_current_timezone_when_no_explicit_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneRegressionTests.test_truncdate_with_fixed_offset_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneRegressionTests.test_trunctime_respects_explicit_tzinfo_over_current db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneRegressionTests.test_trunctime_subquery_with_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneRegressionTests.test_trunctime_uses_current_timezone_when_no_explicit_tzinfo db_functions.datetime.test_extract_trunc_llm.TruncDateTimeZoneRegressionTests.test_trunctime_with_fixed_offset_tzinfo
coverage json -o coverage.json
: '>>>>> End Test Output'
