#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.ManagerWrapsRegressionTests.test_from_queryset_copies_private_method_when_query_only_false basic.tests_llm.ManagerWrapsRegressionTests.test_signature_preserved_for_custom_queryset_method_with_defaults basic.tests_llm.ManagerWrapsRegressionTests.test_signature_preserved_for_existing_queryset_method
coverage json -o coverage.json
: '>>>>> End Test Output'
