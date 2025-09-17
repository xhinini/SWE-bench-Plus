#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.TestJsonScriptFalsyIDs.test_empty_string_id_omitted_for_dict utils_tests.test_html_llm.TestJsonScriptFalsyIDs.test_empty_string_id_omitted_for_empty_value utils_tests.test_html_llm.TestJsonScriptFalsyIDs.test_false_id_omitted utils_tests.test_html_llm.TestJsonScriptFalsyIDs.test_lazy_empty_string_id_omitted utils_tests.test_html_llm.TestJsonScriptFalsyIDs.test_lazy_value_with_empty_id_omitted utils_tests.test_html_llm.TestJsonScriptFalsyIDs.test_mark_safe_empty_string_id_omitted utils_tests.test_html_llm.TestJsonScriptFalsyIDs.test_mark_safe_value_and_empty_id_omitted utils_tests.test_html_llm.TestJsonScriptFalsyIDs.test_zero_id_omitted
coverage json -o coverage.json
: '>>>>> End Test Output'
