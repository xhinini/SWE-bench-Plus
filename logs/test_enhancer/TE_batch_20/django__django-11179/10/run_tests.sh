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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.CollectorSingleInstanceShortcutTests.test_collector_add_returns_new_objs_and_subsequent_delete_sets_pk_none delete.tests_llm.CollectorSingleInstanceShortcutTests.test_collector_delete_returns_zero_if_called_again_with_none_pk delete.tests_llm.CollectorSingleInstanceShortcutTests.test_collector_single_dynamic_model_return_value_and_pk delete.tests_llm.CollectorSingleInstanceShortcutTests.test_collector_single_instance_auto_pk_set_none delete.tests_llm.CollectorSingleInstanceShortcutTests.test_collector_single_instance_bigautofield_pk_set_none delete.tests_llm.CollectorSingleInstanceShortcutTests.test_collector_single_instance_char_pk_set_none delete.tests_llm.CollectorSingleInstanceShortcutTests.test_collector_single_instance_custom_named_pk_set_none delete.tests_llm.CollectorSingleInstanceShortcutTests.test_collector_single_instance_proxy_model_set_pk_none delete.tests_llm.CollectorSingleInstanceShortcutTests.test_collector_single_instance_uuid_pk_set_none
coverage json -o coverage.json
: '>>>>> End Test Output'
