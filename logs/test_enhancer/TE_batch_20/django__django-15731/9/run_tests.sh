#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.FromQuerySetManagerTests.test_copied_method_keeps_doc_and_signature_for_bulk_create_like_method basic.tests_llm.FromQuerySetManagerTests.test_manager_method_is_callable_and_uses_model_for_get_queryset basic.tests_llm.FromQuerySetManagerTests.test_private_methods_copied_when_query_set_flag_false basic.tests_llm.FromQuerySetManagerTests.test_signature_preserved_via___wrapped__
coverage json -o coverage.json
: '>>>>> End Test Output'
