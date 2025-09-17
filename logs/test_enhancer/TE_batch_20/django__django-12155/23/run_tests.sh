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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.ParseDocstringCleandocTests._expected_from_cleandoc admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_10_empty_and_none_like_inputs admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_3_leading_blank_then_indented_title_and_less_indented_body admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_5_first_line_indented_more_and_body_has_trailing_spaces admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_7_first_line_and_body_with_colons_and_indentation admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_case_9_multiple_blank_lines_and_mismatched_indentation
coverage json -o coverage.json
: '>>>>> End Test Output'
