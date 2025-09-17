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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.OptimizerTests.assertDoesNotOptimize migrations.test_optimizer_llm.OptimizerTests.assertOptimizesTo migrations.test_optimizer_llm.OptimizerTests.optimize migrations.test_optimizer_llm.OptimizerTests.serialize migrations.test_optimizer_llm.OptimizerTests.test_create_alter_change_verbose_name migrations.test_optimizer_llm.OptimizerTests.test_create_alter_db_table_in_alter_replaces_and_removes_alter_keys migrations.test_optimizer_llm.OptimizerTests.test_create_alter_empty_options_removes_all_alter_keys migrations.test_optimizer_llm.OptimizerTests.test_create_alter_preserve_permissions_empty_list migrations.test_optimizer_llm.OptimizerTests.test_create_alter_preserves_explicit_false migrations.test_optimizer_llm.OptimizerTests.test_create_alter_preserves_non_alter_keys migrations.test_optimizer_llm.OptimizerTests.test_create_alter_remove_get_latest_by_when_not_present migrations.test_optimizer_llm.OptimizerTests.test_create_alter_removes_unset_alter_keys migrations.test_optimizer_llm.OptimizerTests.test_create_alter_replace_default_manager_name
coverage json -o coverage.json
: '>>>>> End Test Output'
