#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.ManagerSignatureTests.assert_signature_matches_queryset basic.tests_llm.ManagerSignatureTests.test_annotate_preserves_signature_and_wrapped basic.tests_llm.ManagerSignatureTests.test_bulk_create_preserves_wrapped_and_signature basic.tests_llm.ManagerSignatureTests.test_count_preserves_signature_and_wrapped basic.tests_llm.ManagerSignatureTests.test_create_preserves_signature_and_wrapped basic.tests_llm.ManagerSignatureTests.test_exists_preserves_signature_and_wrapped basic.tests_llm.ManagerSignatureTests.test_filter_preserves_signature_and_wrapped basic.tests_llm.ManagerSignatureTests.test_get_preserves_signature_and_wrapped basic.tests_llm.ManagerSignatureTests.test_update_preserves_signature_and_wrapped basic.tests_llm.ManagerSignatureTests.test_values_preserves_signature_and_wrapped
coverage json -o coverage.json
: '>>>>> End Test Output'
