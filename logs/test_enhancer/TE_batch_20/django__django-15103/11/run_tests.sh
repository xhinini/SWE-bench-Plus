#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.test_json_script_empty_bytearray_element_id_omitted utils_tests.test_html_llm.test_json_script_empty_bytes_element_id_omitted utils_tests.test_html_llm.test_json_script_empty_dict_element_id_omitted utils_tests.test_html_llm.test_json_script_empty_list_element_id_omitted utils_tests.test_html_llm.test_json_script_empty_range_element_id_omitted utils_tests.test_html_llm.test_json_script_empty_string_element_id_omitted utils_tests.test_html_llm.test_json_script_empty_tuple_element_id_omitted utils_tests.test_html_llm.test_json_script_false_element_id_omitted utils_tests.test_html_llm.test_json_script_zero_element_id_omitted utils_tests.test_html_llm.test_json_script_zero_float_element_id_omitted
coverage json -o coverage.json
: '>>>>> End Test Output'
