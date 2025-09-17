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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 db_functions.datetime.test_extract_trunc_llm.TruncTZDisabledTests.setUp db_functions.datetime.test_extract_trunc_llm.TruncTZNameTests.setUp db_functions.datetime.test_extract_trunc_llm._DummyCompiler.compile db_functions.datetime.test_extract_trunc_llm._FakeConnection.__init__ db_functions.datetime.test_extract_trunc_llm._FakeOps.datetime_cast_date_sql db_functions.datetime.test_extract_trunc_llm._FakeOps.datetime_cast_time_sql
coverage json -o coverage.json
: '>>>>> End Test Output'
