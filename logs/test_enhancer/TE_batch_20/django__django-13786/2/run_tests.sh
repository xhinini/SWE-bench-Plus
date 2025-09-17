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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_optimizer_llm.test_alter_model_options_add_verbose_name_plural_and_remove_others migrations.test_optimizer_llm.test_alter_model_options_complex_combination migrations.test_optimizer_llm.test_alter_model_options_get_latest_by_removed_when_absent migrations.test_optimizer_llm.test_alter_model_options_handles_boolean_values_and_removes_other_alter_keys migrations.test_optimizer_llm.test_alter_model_options_partial_update_removes_unmentioned_alter_keys migrations.test_optimizer_llm.test_alter_model_options_preserve_key_when_set_to_none migrations.test_optimizer_llm.test_alter_model_options_preserve_non_alter_keys migrations.test_optimizer_llm.test_alter_model_options_preserve_non_alter_with_falsy_value migrations.test_optimizer_llm.test_alter_model_options_remove_all_when_empty migrations.test_optimizer_llm.test_alter_model_options_remove_default_permissions
coverage json -o coverage.json
: '>>>>> End Test Output'
