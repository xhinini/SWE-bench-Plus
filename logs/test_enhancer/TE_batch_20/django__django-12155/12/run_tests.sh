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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.AdminDocsTrimDocstringCleandocTests.test_cleandoc_in_views_globals admin_docs.test_utils_llm.AdminDocsTrimDocstringCleandocTests.test_combined_utils_views_state admin_docs.test_utils_llm.AdminDocsTrimDocstringCleandocTests.test_from_import_trim_docstring_raises admin_docs.test_utils_llm.AdminDocsTrimDocstringCleandocTests.test_getattr_raises_for_trim_docstring admin_docs.test_utils_llm.AdminDocsTrimDocstringCleandocTests.test_trim_docstring_absent_everywhere admin_docs.test_utils_llm.AdminDocsTrimDocstringCleandocTests.test_trim_docstring_not_in_dir admin_docs.test_utils_llm.AdminDocsTrimDocstringCleandocTests.test_trim_docstring_not_in_utils_hasattr admin_docs.test_utils_llm.AdminDocsTrimDocstringCleandocTests.test_views_cleandoc_is_callable admin_docs.test_utils_llm.AdminDocsTrimDocstringCleandocTests.test_views_cleandoc_is_inspect_cleandoc admin_docs.test_utils_llm.AdminDocsTrimDocstringCleandocTests.test_views_has_cleandoc_attribute
coverage json -o coverage.json
: '>>>>> End Test Output'
