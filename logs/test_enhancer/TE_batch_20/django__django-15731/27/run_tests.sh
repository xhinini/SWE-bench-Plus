#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.FakeQuerySet.__init__ basic.tests_llm.FakeQuerySet._private basic.tests_llm.FakeQuerySet.all basic.tests_llm.FakeQuerySet.method_with_varargs basic.tests_llm.FakeQuerySet.proxy_call basic.tests_llm.FakeQuerySet.public_method basic.tests_llm.ManagerFromFakeQSTests.setUp basic.tests_llm.QSWithExplicitUnderscore.__init__ basic.tests_llm.QSWithExplicitUnderscore._exposed_private
coverage json -o coverage.json
: '>>>>> End Test Output'
