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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.TestAdminDocsCleandocUsage.test_utils_has_no_trim_docstring_attribute admin_docs.test_utils_llm.TestAdminDocsCleandocUsage.test_utils_has_no_trim_docstring_definition_in_source admin_docs.test_utils_llm.TestAdminDocsCleandocUsage.test_utils_parse_docstring_uses_cleandoc_in_source admin_docs.test_utils_llm.TestAdminDocsCleandocUsage.test_views_does_not_reference_trim_docstring admin_docs.test_utils_llm.TestAdminDocsCleandocUsage.test_views_module_imports_cleandoc admin_docs.test_utils_llm.TestAdminDocsCleandocUsage.test_views_source_uses_cleandoc
coverage json -o coverage.json
: '>>>>> End Test Output'
