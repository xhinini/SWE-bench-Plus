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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.CreateModelAlterOptionsReduceTests._reduced_options migrations.test_optimizer_llm.CreateModelAlterOptionsReduceTests.test_add_new_alter_option_key migrations.test_optimizer_llm.CreateModelAlterOptionsReduceTests.test_default_permissions_removed_when_not_in_alter migrations.test_optimizer_llm.CreateModelAlterOptionsReduceTests.test_empty_list_value_is_preserved migrations.test_optimizer_llm.CreateModelAlterOptionsReduceTests.test_mix_of_removals_and_updates migrations.test_optimizer_llm.CreateModelAlterOptionsReduceTests.test_preserve_alter_key_even_if_value_is_none migrations.test_optimizer_llm.CreateModelAlterOptionsReduceTests.test_preserve_non_alter_option_keys migrations.test_optimizer_llm.CreateModelAlterOptionsReduceTests.test_remove_get_latest_by_when_not_provided migrations.test_optimizer_llm.CreateModelAlterOptionsReduceTests.test_remove_managed_but_keep_custom_keys migrations.test_optimizer_llm.CreateModelAlterOptionsReduceTests.test_remove_multiple_alter_option_keys_not_present migrations.test_optimizer_llm.CreateModelAlterOptionsReduceTests.test_remove_ordering_when_alter_options_empty
coverage json -o coverage.json
: '>>>>> End Test Output'
