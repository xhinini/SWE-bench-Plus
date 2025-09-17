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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.TestModelDetailDocstringCleaning._run_and_capture_parsed admin_docs.test_utils_llm.TestModelDetailDocstringCleaning.assert_docstring_cleaned_and_used admin_docs.test_utils_llm.TestModelDetailDocstringCleaning.make_model_with_callable admin_docs.test_utils_llm.TestModelDetailDocstringCleaning.test_method_docstring_first_line_less_indented_than_second admin_docs.test_utils_llm.TestModelDetailDocstringCleaning.test_method_docstring_first_line_more_indented_than_second admin_docs.test_utils_llm.TestModelDetailDocstringCleaning.test_method_docstring_none_docstring_results_in_empty_pass_to_parse_rst admin_docs.test_utils_llm.TestModelDetailDocstringCleaning.test_method_docstring_single_line_with_leading_spaces admin_docs.test_utils_llm.TestModelDetailDocstringCleaning.test_method_docstring_with_leading_blank_line_and_indentation admin_docs.test_utils_llm.TestModelDetailDocstringCleaning.test_method_docstring_with_mixed_spaces_and_tabs admin_docs.test_utils_llm.TestModelDetailDocstringCleaning.test_method_docstring_with_multiple_internal_blank_lines admin_docs.test_utils_llm.TestModelDetailDocstringCleaning.test_method_docstring_with_trailing_spaces admin_docs.test_utils_llm.TestModelDetailDocstringCleaning.test_property_docstring_indentation_preserved_by_cleandoc admin_docs.test_utils_llm.TestModelDetailDocstringCleaning.test_property_docstring_single_line
coverage json -o coverage.json
: '>>>>> End Test Output'
