#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.JsonScriptOptionalIdTests._expected utils_tests.test_html_llm.JsonScriptOptionalIdTests.test_empty_string_id_with_dict_value utils_tests.test_html_llm.JsonScriptOptionalIdTests.test_empty_string_id_with_lazy_value utils_tests.test_html_llm.JsonScriptOptionalIdTests.test_empty_string_id_with_list_value utils_tests.test_html_llm.JsonScriptOptionalIdTests.test_empty_string_id_with_string_value utils_tests.test_html_llm.JsonScriptOptionalIdTests.test_false_id_with_dict_value utils_tests.test_html_llm.JsonScriptOptionalIdTests.test_false_id_with_lazy_value utils_tests.test_html_llm.JsonScriptOptionalIdTests.test_false_id_with_string_value utils_tests.test_html_llm.JsonScriptOptionalIdTests.test_zero_id_with_dict_value utils_tests.test_html_llm.JsonScriptOptionalIdTests.test_zero_id_with_lazy_value utils_tests.test_html_llm.JsonScriptOptionalIdTests.test_zero_id_with_string_value
coverage json -o coverage.json
: '>>>>> End Test Output'
