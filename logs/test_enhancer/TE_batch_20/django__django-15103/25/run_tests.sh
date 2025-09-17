#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.JsonScriptElementIDTests.test_json_script_empty_string_value_and_empty_id utils_tests.test_html_llm.JsonScriptElementIDTests.test_json_script_omits_empty_string_id utils_tests.test_html_llm.JsonScriptElementIDTests.test_json_script_omits_false_id utils_tests.test_html_llm.JsonScriptElementIDTests.test_json_script_omits_zero_id
coverage json -o coverage.json
: '>>>>> End Test Output'
