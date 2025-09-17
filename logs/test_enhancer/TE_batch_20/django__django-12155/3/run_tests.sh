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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.ParseDocstringIndentationTests.test_body_with_internal_blank_lines_keeps_structure_and_indentation admin_docs.test_utils_llm.ParseDocstringIndentationTests.test_first_line_less_indented_preserves_body_indentation admin_docs.test_utils_llm.ParseDocstringIndentationTests.test_first_line_more_indented_than_empty_lines admin_docs.test_utils_llm.ParseDocstringIndentationTests.test_first_line_no_indent_keeps_body_fully_indented admin_docs.test_utils_llm.ParseDocstringIndentationTests.test_metadata_parsing_with_indented_body admin_docs.test_utils_llm.ParseDocstringIndentationTests.test_multiple_body_lines_preserve_common_indentation
coverage json -o coverage.json
: '>>>>> End Test Output'
