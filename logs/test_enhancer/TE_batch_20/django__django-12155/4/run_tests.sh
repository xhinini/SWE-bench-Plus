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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_parse_docstring_with_tabs_and_spaces_matches_cleandoc admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_parse_rst_handles_directive_first_line_and_parses_roles admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_parse_rst_on_parsed_docstring_does_not_emit_stderr
coverage json -o coverage.json
: '>>>>> End Test Output'
