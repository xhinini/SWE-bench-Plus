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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.AlterModelOptionsReduceTests._assertOptimizesTo migrations.test_optimizer_llm.AlterModelOptionsReduceTests.optimize migrations.test_optimizer_llm.AlterModelOptionsReduceTests.serialize migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_add_non_alter_key_and_remove_alter_keys migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_empty_list_value_is_kept_for_permissions migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_keep_key_present_with_none_value migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_keep_only_specified_alter_keys migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_no_initial_options_but_add_non_alter_option migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_overwrite_non_alter_key_and_remove_alters migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_preserve_custom_non_alter_option_when_removing_alters migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_preserve_non_alter_keys_when_updating_alter_key migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_remove_all_alter_option_keys_when_empty migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_update_one_alter_key_and_remove_others
coverage json -o coverage.json
: '>>>>> End Test Output'
