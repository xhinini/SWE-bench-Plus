#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.ImportWhitespaceTests._run_test_with_import migrations.test_writer_llm.ImportWhitespaceTests.test_from_uppercase migrations.test_writer_llm.ImportWhitespaceTests.test_from_with_extra_spaces migrations.test_writer_llm.ImportWhitespaceTests.test_from_with_leading_space migrations.test_writer_llm.ImportWhitespaceTests.test_from_with_leading_tab migrations.test_writer_llm.ImportWhitespaceTests.test_import_prefixed_by_newline migrations.test_writer_llm.ImportWhitespaceTests.test_import_uppercase migrations.test_writer_llm.ImportWhitespaceTests.test_import_with_leading_space migrations.test_writer_llm.ImportWhitespaceTests.test_import_with_leading_tab migrations.test_writer_llm.ImportWhitespaceTests.test_import_with_multiple_leading_spaces migrations.test_writer_llm.ImportWhitespaceTests.test_import_with_tab_between_keyword_and_module
coverage json -o coverage.json
: '>>>>> End Test Output'
