#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.ManagerWrapsTests.test_get_queryset_methods_excludes_private_methods basic.tests_llm.ManagerWrapsTests.test_module_has_wraps basic.tests_llm.ManagerWrapsTests.test_signature_matches_queryset_bulk_create
coverage json -o coverage.json
: '>>>>> End Test Output'
