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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.TestUtilsTrimIntegration._make_fake_model_with_property admin_docs.test_utils_llm.TestUtilsTrimIntegration._raise_if_trim_called admin_docs.test_utils_llm.TestUtilsTrimIntegration.test_model_detail_property_and_method_together_do_not_call_trim admin_docs.test_utils_llm.TestUtilsTrimIntegration.test_model_detail_uses_cleandoc_for_method_docstring admin_docs.test_utils_llm.TestUtilsTrimIntegration.test_model_detail_uses_cleandoc_for_property_docstring admin_docs.test_utils_llm.TestUtilsTrimIntegration.test_parse_docstring_does_not_call_trim_on_simple_docstring admin_docs.test_utils_llm.TestUtilsTrimIntegration.test_parse_docstring_does_not_call_trim_with_indented_docstring admin_docs.test_utils_llm.TestUtilsTrimIntegration.test_parse_docstring_handles_none_without_calling_trim admin_docs.test_utils_llm.TestUtilsTrimIntegration.test_parse_docstring_multiline_metadata_parsing admin_docs.test_utils_llm.TestUtilsTrimIntegration.test_parse_docstring_with_leading_blank_and_indented_block
coverage json -o coverage.json
: '>>>>> End Test Output'
