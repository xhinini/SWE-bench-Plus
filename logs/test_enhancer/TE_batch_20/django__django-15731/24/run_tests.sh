#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.FromQuerysetCopyingBehaviorTests.test_from_queryset_copies_custom_method_signature_and_doc basic.tests_llm.FromQuerysetCopyingBehaviorTests.test_manager_bound_and_unbound_signatures_match_queryset
coverage json -o coverage.json
: '>>>>> End Test Output'
