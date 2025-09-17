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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.AdmindocsUtilsRegressionTests.test_no_trim_docstring_definition_in_utils_source admin_docs.test_utils_llm.AdmindocsUtilsRegressionTests.test_trim_docstring_attribute_removed admin_docs.test_utils_llm.AdmindocsUtilsRegressionTests.test_utils_uses_cleandoc admin_docs.test_utils_llm.AdmindocsUtilsRegressionTests.test_views_does_not_call_utils_trim_docstring admin_docs.test_utils_llm.AdmindocsUtilsRegressionTests.test_views_uses_cleandoc_for_method_verbose
coverage json -o coverage.json
: '>>>>> End Test Output'
