#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_html_llm.JsonScriptFalsyElementIdTests.check_omits_id utils_tests.test_html_llm.JsonScriptFalsyElementIdTests.test_empty_bytearray_omits_id utils_tests.test_html_llm.JsonScriptFalsyElementIdTests.test_empty_bytes_omits_id utils_tests.test_html_llm.JsonScriptFalsyElementIdTests.test_empty_dict_omits_id utils_tests.test_html_llm.JsonScriptFalsyElementIdTests.test_empty_list_omits_id utils_tests.test_html_llm.JsonScriptFalsyElementIdTests.test_empty_set_omits_id utils_tests.test_html_llm.JsonScriptFalsyElementIdTests.test_empty_string_omits_id utils_tests.test_html_llm.JsonScriptFalsyElementIdTests.test_empty_tuple_omits_id utils_tests.test_html_llm.JsonScriptFalsyElementIdTests.test_false_bool_omits_id utils_tests.test_html_llm.JsonScriptFalsyElementIdTests.test_lazy_empty_string_omits_id utils_tests.test_html_llm.JsonScriptFalsyElementIdTests.test_zero_int_omits_id
coverage json -o coverage.json
: '>>>>> End Test Output'
