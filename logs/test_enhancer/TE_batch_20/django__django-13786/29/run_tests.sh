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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.AlterModelOptionsReduceTests.assertOptimizesTo migrations.test_optimizer_llm.AlterModelOptionsReduceTests.optimize migrations.test_optimizer_llm.AlterModelOptionsReduceTests.serialize migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_alter_adds_new_alter_key_and_removes_absent_ones migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_alter_creates_alter_keys_when_initial_empty migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_alter_with_none_value_keeps_key migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_empty_alter_removes_all_alter_keys_but_preserves_non_alter migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_false_values_in_alter_keys_are_removed_when_absent migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_multiple_alter_keys_subset_kept_others_removed migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_non_alter_key_update_preserved_and_alter_removed migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_non_alter_preserved_with_alter_change migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_partial_alter_removes_other_alter_keys migrations.test_optimizer_llm.AlterModelOptionsReduceTests.test_preserve_custom_non_alter_keys
coverage json -o coverage.json
: '>>>>> End Test Output'
