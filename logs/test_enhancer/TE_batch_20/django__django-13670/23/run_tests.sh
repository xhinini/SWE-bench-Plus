#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 utils_tests.test_dateformat_llm.test_date_object_y_padding utils_tests.test_dateformat_llm.test_escaped_y_not_interpreted utils_tests.test_dateformat_llm.test_expected_values_for_some_edge_years utils_tests.test_dateformat_llm.test_multiple_y_repeats utils_tests.test_dateformat_llm.test_wrapper_and_module_format_agree utils_tests.test_dateformat_llm.test_y_output_length_two_for_various_years utils_tests.test_dateformat_llm.test_y_padding_single_digit utils_tests.test_dateformat_llm.test_y_padding_year_100 utils_tests.test_dateformat_llm.test_y_padding_year_1000 utils_tests.test_dateformat_llm.test_y_padding_year_2000
coverage json -o coverage.json
: '>>>>> End Test Output'
