#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 basic.tests_llm.ManagerWrapsRegressionTests.test_existing_manager_methods_not_overridden basic.tests_llm.ManagerWrapsRegressionTests.test_from_queryset_adds_methods_to_manager_class basic.tests_llm.ManagerWrapsRegressionTests.test_manager_method_calls_underlying_queryset basic.tests_llm.ManagerWrapsRegressionTests.test_multiple_custom_methods_kept basic.tests_llm.ManagerWrapsRegressionTests.test_private_methods_are_not_copied_and_queryet_only_flag_respected basic.tests_llm.ManagerWrapsRegressionTests.test_queryset_only_attribute_on_a_real_method_blocks_copy basic.tests_llm.ManagerWrapsRegressionTests.test_signature_preserved_for_bulk_create_and_filter basic.tests_llm.ManagerWrapsRegressionTests.test_wrapped_attributes_preserved_for_common_methods basic.tests_llm.ManagerWrapsRegressionTests.test_wrappers_are_regular_functions_and_inspectable
coverage json -o coverage.json
: '>>>>> End Test Output'
