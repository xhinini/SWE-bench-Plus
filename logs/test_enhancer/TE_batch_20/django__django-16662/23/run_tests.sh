#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.WeirdImportTests._make_migration_with_weird_import migrations.test_writer_llm.WeirdImportTests.test_double_space_after_from migrations.test_writer_llm.WeirdImportTests.test_double_space_and_models migrations.test_writer_llm.WeirdImportTests.test_leading_space_before_from migrations.test_writer_llm.WeirdImportTests.test_leading_spaces_and_double_after_from migrations.test_writer_llm.WeirdImportTests.test_leading_tab_before_from migrations.test_writer_llm.WeirdImportTests.test_multiple_weird_imports_present migrations.test_writer_llm.WeirdImportTests.test_tab_after_from migrations.test_writer_llm.WeirdImportTests.test_unregister_serializer_removes_behavior migrations.test_writer_llm.WeirdImportTests.test_weird_imports_and_standard_import_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
