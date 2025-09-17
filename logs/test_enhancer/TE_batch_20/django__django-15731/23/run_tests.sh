#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.ManagerWrapsRegressionTests.test_doc_and_signature_for_dynamic_from_queryset_methods basic.tests_llm.ManagerWrapsRegressionTests.test_signature_preserved_for_bulk_create_like_method basic.tests_llm.ManagerWrapsRegressionTests.test_signature_with_varied_parameters
coverage json -o coverage.json
: '>>>>> End Test Output'
