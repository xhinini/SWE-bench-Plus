#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.ImportOrderingTests._get_import_block migrations.test_writer_llm.ImportOrderingTests.test_complex_mixture_sorting migrations.test_writer_llm.ImportOrderingTests.test_from_imports_after_imports_with_settings migrations.test_writer_llm.ImportOrderingTests.test_import_order_with_only_froms migrations.test_writer_llm.ImportOrderingTests.test_imports_all_imports_sorted_before_froms_even_when_many migrations.test_writer_llm.ImportOrderingTests.test_imports_grouped_simple migrations.test_writer_llm.ImportOrderingTests.test_imports_order_with_similar_module_names migrations.test_writer_llm.ImportOrderingTests.test_imports_sorted_alphabetically_multiple_modules migrations.test_writer_llm.ImportOrderingTests.test_merged_django_db_models_line_present migrations.test_writer_llm.ImportOrderingTests.test_mixed_prefixes_sorting migrations.test_writer_llm.ImportOrderingTests.test_no_from_before_import
coverage json -o coverage.json
: '>>>>> End Test Output'
