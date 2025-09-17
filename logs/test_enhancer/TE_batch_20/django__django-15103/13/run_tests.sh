#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_empty_bytes_id_results_in_no_id_attribute utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_empty_list_id_results_in_no_id_attribute utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_empty_string_id_results_in_no_id_attribute utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_escaping_preserved_when_no_id utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_false_id_results_in_no_id_attribute utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_lazy_empty_string_id_results_in_no_id_attribute utils_tests.test_html_llm.JsonScriptFalsyIdTests.test_zero_id_results_in_no_id_attribute
coverage json -o coverage.json
: '>>>>> End Test Output'
