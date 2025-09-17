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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.ParseDocstringCleandocTests._install_and_count_cleandoc admin_docs.test_utils_llm.ParseDocstringCleandocTests._restore_cleandoc admin_docs.test_utils_llm.ParseDocstringCleandocTests.setUp admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_parse_docstring_uses_cleandoc_complex_indentation admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_parse_docstring_uses_cleandoc_multiline admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_parse_docstring_uses_cleandoc_multiple_paragraphs admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_parse_docstring_uses_cleandoc_simple admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_parse_docstring_uses_cleandoc_when_metadata_present admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_parse_docstring_uses_cleandoc_when_only_body admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_parse_docstring_uses_cleandoc_with_leading_newline admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_parse_docstring_uses_cleandoc_with_tabs admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_parse_docstring_uses_cleandoc_with_unicode admin_docs.test_utils_llm.ParseDocstringCleandocTests.test_trim_docstring_removed
coverage json -o coverage.json
: '>>>>> End Test Output'
