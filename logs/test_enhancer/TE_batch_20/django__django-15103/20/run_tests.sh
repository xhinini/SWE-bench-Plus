#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.test_json_script_dict_with_empty_id_maintains_escaping utils_tests.test_html_llm.test_json_script_includes_id_for_string_zero utils_tests.test_html_llm.test_json_script_includes_id_for_true utils_tests.test_html_llm.test_json_script_lazy_value_with_empty_id utils_tests.test_html_llm.test_json_script_omits_id_when_empty_list utils_tests.test_html_llm.test_json_script_omits_id_when_empty_string utils_tests.test_html_llm.test_json_script_omits_id_when_empty_tuple utils_tests.test_html_llm.test_json_script_omits_id_when_false utils_tests.test_html_llm.test_json_script_omits_id_when_zero_float utils_tests.test_html_llm.test_json_script_omits_id_when_zero_int
coverage json -o coverage.json
: '>>>>> End Test Output'
