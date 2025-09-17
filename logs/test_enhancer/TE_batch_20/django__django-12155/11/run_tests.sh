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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_docs.test_utils_llm.TestAdmindocsParsingAndModelDetail._get_model_fields_verbose admin_docs.test_utils_llm.TestAdmindocsParsingAndModelDetail._register_model admin_docs.test_utils_llm.TestAdmindocsParsingAndModelDetail.setUp admin_docs.test_utils_llm.TestAdmindocsParsingAndModelDetail.tearDown admin_docs.test_utils_llm.TestAdmindocsParsingAndModelDetail.test_model_method_docstring_is_dedented_and_rendered admin_docs.test_utils_llm.TestAdmindocsParsingAndModelDetail.test_model_method_with_leading_newline_docstring admin_docs.test_utils_llm.TestAdmindocsParsingAndModelDetail.test_model_property_docstring_dedented_and_rendered admin_docs.test_utils_llm.TestAdmindocsParsingAndModelDetail.test_multiple_methods_various_doc_indent
coverage json -o coverage.json
: '>>>>> End Test Output'
