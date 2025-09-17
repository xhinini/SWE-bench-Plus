#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_create_alter_managers_and_options_merge_order1 migrations.test_optimizer_llm.test_create_alter_managers_nonmatching_name_no_absorb migrations.test_optimizer_llm.test_create_managers_and_addfield_combined migrations.test_optimizer_llm.test_create_managers_case_insensitive_name migrations.test_optimizer_llm.test_create_managers_with_alter_index_together migrations.test_optimizer_llm.test_create_managers_with_altertogether_option migrations.test_optimizer_llm.test_create_multiple_alter_managers_last_wins migrations.test_optimizer_llm.test_create_options_then_managers_merge_order2 migrations.test_optimizer_llm.test_create_rename_then_alter_managers_merges
coverage json -o coverage.json
: '>>>>> End Test Output'
