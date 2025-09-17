#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.ImportPreserveTests._run_with_import_line migrations.test_writer_llm.ImportPreserveTests.test_preserve_c_style_comment_line migrations.test_writer_llm.ImportPreserveTests.test_preserve_comment_import_line migrations.test_writer_llm.ImportPreserveTests.test_preserve_from_keyword_only_line migrations.test_writer_llm.ImportPreserveTests.test_preserve_from_no_space_line migrations.test_writer_llm.ImportPreserveTests.test_preserve_import_keyword_only_line migrations.test_writer_llm.ImportPreserveTests.test_preserve_import_with_tab_between migrations.test_writer_llm.ImportPreserveTests.test_preserve_leading_space_import_line migrations.test_writer_llm.ImportPreserveTests.test_preserve_leading_tab_import_line migrations.test_writer_llm.ImportPreserveTests.test_preserve_missing_from_prefix_line migrations.test_writer_llm.ImportPreserveTests.test_preserve_uppercase_import_line
coverage json -o coverage.json
: '>>>>> End Test Output'
