#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.ManagerWrappingTests.test_decorated_queryset_method_preserves_original_signature basic.tests_llm.ManagerWrappingTests.test_signature_bulk_create_preserved basic.tests_llm.ManagerWrappingTests.test_signature_update_preserved
coverage json -o coverage.json
: '>>>>> End Test Output'
