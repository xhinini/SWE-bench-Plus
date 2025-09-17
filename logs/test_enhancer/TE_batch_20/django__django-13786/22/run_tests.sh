#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
python --version && python -m pip install -U pip
python -m pip install -U 'coverage==6.2'

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_create_alter_model_options_does_not_remove_non_alter_when_alter_is_empty migrations.test_optimizer_llm.test_create_alter_model_options_empty_removes_all_alter_but_preserves_non_alter migrations.test_optimizer_llm.test_create_alter_model_options_handles_empty_permissions_set migrations.test_optimizer_llm.test_create_alter_model_options_keeps_explicit_false migrations.test_optimizer_llm.test_create_alter_model_options_keeps_explicit_none migrations.test_optimizer_llm.test_create_alter_model_options_merges_multiple_keys migrations.test_optimizer_llm.test_create_alter_model_options_preserves_non_alter_db_table migrations.test_optimizer_llm.test_create_alter_model_options_removes_ordering_permissions_empty migrations.test_optimizer_llm.test_create_alter_model_options_removes_unmentioned_alter_keys migrations.test_optimizer_llm.test_create_alter_model_options_sequential_alter_ops
coverage json -o coverage.json
: '>>>>> End Test Output'
