#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.ImportSortingTests._as_string_for_ops migrations.test_writer_llm.ImportSortingTests.test_filename_and_path_properties migrations.test_writer_llm.ImportSortingTests.test_group_imports_and_ordering migrations.test_writer_llm.ImportSortingTests.test_header_inclusion_control migrations.test_writer_llm.ImportSortingTests.test_imports_grouping_with_custom_operations migrations.test_writer_llm.ImportSortingTests.test_imports_order_with_varied_modules migrations.test_writer_llm.ImportSortingTests.test_migration_imports_become_comment_block migrations.test_writer_llm.ImportSortingTests.test_models_import_merged_with_migrations migrations.test_writer_llm.ImportSortingTests.test_multiple_from_same_module_present migrations.test_writer_llm.ImportSortingTests.test_swappable_dependency_includes_settings_import
coverage json -o coverage.json
: '>>>>> End Test Output'
