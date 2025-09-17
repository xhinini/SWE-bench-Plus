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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 cache.tests_llm.CullTests.setUp cache.tests_llm.FakeConnection.__init__ cache.tests_llm.FakeCursor.__enter__ cache.tests_llm.FakeCursor.__exit__ cache.tests_llm.FakeCursor.__init__ cache.tests_llm.FakeCursor.execute cache.tests_llm.FakeCursor.fetchone cache.tests_llm.FakeOps.__init__ cache.tests_llm.FakeOps.adapt_datetimefield_value cache.tests_llm.FakeOps.cache_key_culling_sql cache.tests_llm.FakeOps.quote_name
coverage json -o coverage.json
: '>>>>> End Test Output'
