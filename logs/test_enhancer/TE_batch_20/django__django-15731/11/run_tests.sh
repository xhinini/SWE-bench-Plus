#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.ManagerMetadataRegressionTests.assert_method_metadata_preserved basic.tests_llm.ManagerMetadataRegressionTests.test_bulk_create_metadata basic.tests_llm.ManagerMetadataRegressionTests.test_dynamic_from_queryset_preserves_signature_and_wrapped basic.tests_llm.ManagerMetadataRegressionTests.test_filter_metadata basic.tests_llm.ManagerMetadataRegressionTests.test_get_metadata basic.tests_llm.ManagerMetadataRegressionTests.test_none_metadata basic.tests_llm.ManagerMetadataRegressionTests.test_order_by_metadata basic.tests_llm.ManagerMetadataRegressionTests.test_update_metadata basic.tests_llm.ManagerMetadataRegressionTests.test_values_list_metadata basic.tests_llm.ManagerMetadataRegressionTests.test_values_metadata
coverage json -o coverage.json
: '>>>>> End Test Output'
