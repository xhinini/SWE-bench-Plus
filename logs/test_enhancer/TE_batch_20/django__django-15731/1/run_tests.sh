#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.ManagerWrapsTests.test_bulk_create_signature_matches_queryset basic.tests_llm.ManagerWrapsTests.test_filter_signature_and_doc basic.tests_llm.ManagerWrapsTests.test_from_queryset_preserves_signature_and_doc basic.tests_llm.ManagerWrapsTests.test_update_signature_and_doc basic.tests_llm.ManagerWrapsTests.test_wrapped_chain_preserves_original_function_signature
coverage json -o coverage.json
: '>>>>> End Test Output'
