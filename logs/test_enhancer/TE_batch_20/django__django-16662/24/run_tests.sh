#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_writer_llm.LeadingImportTests.make_output_with_import migrations.test_writer_llm.LeadingImportTests.setUp migrations.test_writer_llm.LeadingImportTests.test_double_leading_tab migrations.test_writer_llm.LeadingImportTests.test_four_leading_spaces migrations.test_writer_llm.LeadingImportTests.test_leading_carriage_return migrations.test_writer_llm.LeadingImportTests.test_leading_crlf migrations.test_writer_llm.LeadingImportTests.test_leading_newline migrations.test_writer_llm.LeadingImportTests.test_leading_tab migrations.test_writer_llm.LeadingImportTests.test_mixed_space_tab migrations.test_writer_llm.LeadingImportTests.test_newline_then_tab migrations.test_writer_llm.LeadingImportTests.test_single_leading_space migrations.test_writer_llm.LeadingImportTests.test_two_leading_spaces
coverage json -o coverage.json
: '>>>>> End Test Output'
