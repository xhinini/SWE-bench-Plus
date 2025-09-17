#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.JsonScriptElementIdTests.test_dict_value_escaped_and_no_id_for_empty_element utils_tests.test_html_llm.JsonScriptElementIdTests.test_empty_bytes_element_id_produces_no_id_attribute utils_tests.test_html_llm.JsonScriptElementIdTests.test_empty_string_element_id_produces_no_id_attribute utils_tests.test_html_llm.JsonScriptElementIdTests.test_empty_string_element_id_with_escaped_content utils_tests.test_html_llm.JsonScriptElementIdTests.test_false_element_id_produces_no_id_attribute utils_tests.test_html_llm.JsonScriptElementIdTests.test_false_element_id_with_complex_value_has_no_id_and_is_escaped utils_tests.test_html_llm.JsonScriptElementIdTests.test_zero_int_element_id_produces_no_id_attribute
coverage json -o coverage.json
: '>>>>> End Test Output'
