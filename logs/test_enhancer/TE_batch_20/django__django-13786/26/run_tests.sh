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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.CreateModelAlterOptionsReductionTests._reduce migrations.test_optimizer_llm.CreateModelAlterOptionsReductionTests.test_add_new_alter_option_and_remove_others migrations.test_optimizer_llm.CreateModelAlterOptionsReductionTests.test_alter_does_not_remove_other_custom_keys migrations.test_optimizer_llm.CreateModelAlterOptionsReductionTests.test_alter_with_index_and_permissions_behavior migrations.test_optimizer_llm.CreateModelAlterOptionsReductionTests.test_combined_non_alter_and_alter_key_modification migrations.test_optimizer_llm.CreateModelAlterOptionsReductionTests.test_empty_alter_removes_all_alter_option_keys migrations.test_optimizer_llm.CreateModelAlterOptionsReductionTests.test_falsey_values_are_preserved_when_present migrations.test_optimizer_llm.CreateModelAlterOptionsReductionTests.test_merge_overwrites_values migrations.test_optimizer_llm.CreateModelAlterOptionsReductionTests.test_multiple_alter_keys_some_removed_some_kept migrations.test_optimizer_llm.CreateModelAlterOptionsReductionTests.test_preserve_non_alter_options migrations.test_optimizer_llm.CreateModelAlterOptionsReductionTests.test_remove_unmentioned_alter_option_keys
coverage json -o coverage.json
: '>>>>> End Test Output'
