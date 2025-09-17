#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.ManagerWrappingAdditionalTests.test_manager_method_signature_matches_queryset basic.tests_llm.ManagerWrappingAdditionalTests.test_signature_of_bulk_create_matches_queryset
coverage json -o coverage.json
: '>>>>> End Test Output'
