#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.ImportSortingTests._make_migration migrations.test_writer_llm.ImportSortingTests.test_combined_import_sorting migrations.test_writer_llm.ImportSortingTests.test_custom_and_builtin_imports_present migrations.test_writer_llm.ImportSortingTests.test_from_statements_alphabetical migrations.test_writer_llm.ImportSortingTests.test_imports_alphabetical_within_imports migrations.test_writer_llm.ImportSortingTests.test_imports_grouping_import_before_from migrations.test_writer_llm.ImportSortingTests.test_imports_stable_across_calls migrations.test_writer_llm.ImportSortingTests.test_migration_imports_comment_present migrations.test_writer_llm.ImportSortingTests.test_models_merged_with_migrations_and_placement migrations.test_writer_llm.ImportSortingTests.test_swappable_dependency_adds_settings_import
coverage json -o coverage.json
: '>>>>> End Test Output'
