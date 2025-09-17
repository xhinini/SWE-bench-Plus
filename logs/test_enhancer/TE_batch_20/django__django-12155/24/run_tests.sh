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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.TestModelDocstringDedent._assert_not_literal admin_docs.test_utils_llm.TestModelDocstringDedent._get_verbose admin_docs.test_utils_llm.TestModelDocstringDedent._make_model_with_doc admin_docs.test_utils_llm.TestModelDocstringDedent.setUp admin_docs.test_utils_llm.TestModelDocstringDedent.test_first_line_indented_followed_by_indented_paragraph admin_docs.test_utils_llm.TestModelDocstringDedent.test_indented_block_after_blank_line admin_docs.test_utils_llm.TestModelDocstringDedent.test_indented_line_with_backticks admin_docs.test_utils_llm.TestModelDocstringDedent.test_indented_param_like_line admin_docs.test_utils_llm.TestModelDocstringDedent.test_leading_blank_line_then_indented admin_docs.test_utils_llm.TestModelDocstringDedent.test_leading_role_directive_with_indented_body admin_docs.test_utils_llm.TestModelDocstringDedent.test_mixed_two_space_indentation admin_docs.test_utils_llm.TestModelDocstringDedent.test_no_docstring admin_docs.test_utils_llm.TestModelDocstringDedent.test_property_docstring_with_indented_content admin_docs.test_utils_llm.TestModelDocstringDedent.test_single_indented_line_only
coverage json -o coverage.json
: '>>>>> End Test Output'
