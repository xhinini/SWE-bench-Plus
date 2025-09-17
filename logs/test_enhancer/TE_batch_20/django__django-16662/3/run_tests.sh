#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.ImportOrderingTests.index_of migrations.test_writer_llm.ImportOrderingTests.make_migration_with_ops migrations.test_writer_llm.ImportOrderingTests.test_builtin_module_import_ordering migrations.test_writer_llm.ImportOrderingTests.test_decimal_vs_conf_from_order migrations.test_writer_llm.ImportOrderingTests.test_from_imports_order_by_module migrations.test_writer_llm.ImportOrderingTests.test_import_statements_sorted_lexicographically migrations.test_writer_llm.ImportOrderingTests.test_imports_and_froms_do_not_interleave migrations.test_writer_llm.ImportOrderingTests.test_imports_before_from_grouping migrations.test_writer_llm.ImportOrderingTests.test_many_imports_sorting_stability migrations.test_writer_llm.ImportOrderingTests.test_mixed_imports_and_froms_overall_ordering migrations.test_writer_llm.ImportOrderingTests.test_same_module_from_variants_ordering
coverage json -o coverage.json
: '>>>>> End Test Output'
