#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_dateformat_llm.test_Y_boundary_year_1000 utils_tests.test_dateformat_llm.test_Y_method_on_date_year_123 utils_tests.test_dateformat_llm.test_Y_method_on_datetime_year_123 utils_tests.test_dateformat_llm.test_Y_padding_various_years utils_tests.test_dateformat_llm.test_combined_format_Y_md utils_tests.test_dateformat_llm.test_concatenation_works_and_is_string utils_tests.test_dateformat_llm.test_direct_method_type_is_str utils_tests.test_dateformat_llm.test_format_convenience_returns_padded_string utils_tests.test_dateformat_llm.test_format_with_escape_preserves_literal_Y utils_tests.test_dateformat_llm.test_multiple_Y_tokens_consistency
coverage json -o coverage.json
: '>>>>> End Test Output'
