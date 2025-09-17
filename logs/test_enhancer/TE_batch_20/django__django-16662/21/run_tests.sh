#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.OpWithValue.__init__ migrations.test_writer_llm.OpWithValue.deconstruct migrations.test_writer_llm.TestImportSorting._build_migration_and_output migrations.test_writer_llm.TestImportSorting._register_serializer migrations.test_writer_llm.TestImportSorting.test_complex_mixture_of_many_imports migrations.test_writer_llm.TestImportSorting.test_duplicate_imports_and_deduplication migrations.test_writer_llm.TestImportSorting.test_group_imports_and_from_statements_order_basic migrations.test_writer_llm.TestImportSorting.test_imports_with_multiple_names_in_from migrations.test_writer_llm.TestImportSorting.test_long_module_names_ordering migrations.test_writer_llm.TestImportSorting.test_migration_imports_become_comment migrations.test_writer_llm.TestImportSorting.test_mixed_case_sorting_behavior migrations.test_writer_llm.TestImportSorting.test_models_merge_and_order migrations.test_writer_llm.TestImportSorting.test_sorting_imports_by_module_name migrations.test_writer_llm.TestImportSorting.test_subpackage_sorting
coverage json -o coverage.json
: '>>>>> End Test Output'
