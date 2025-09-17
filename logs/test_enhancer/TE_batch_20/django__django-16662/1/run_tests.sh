#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.ImportOrderingTests._render migrations.test_writer_llm.ImportOrderingTests.test_custom_and_stdlib_imports_grouping migrations.test_writer_llm.ImportOrderingTests.test_custom_operation_imports_ordering migrations.test_writer_llm.ImportOrderingTests.test_duplicate_imports_and_merge_behavior migrations.test_writer_llm.ImportOrderingTests.test_from_imports_sorted_by_module migrations.test_writer_llm.ImportOrderingTests.test_imports_grouping_imports_before_from migrations.test_writer_llm.ImportOrderingTests.test_imports_include_uuid_and_pathlib_and_are_sorted migrations.test_writer_llm.ImportOrderingTests.test_models_import_merged_with_migrations migrations.test_writer_llm.ImportOrderingTests.test_multiple_from_statements_ordering migrations.test_writer_llm.ImportOrderingTests.test_swappable_dependency_adds_settings_import_and_is_grouped
coverage json -o coverage.json
: '>>>>> End Test Output'
