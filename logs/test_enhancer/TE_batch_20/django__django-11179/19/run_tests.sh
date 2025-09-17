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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 delete.tests_llm.FastDeletePkRegressionTests.test_collector_can_fast_delete_reflects_after_delete_state delete.tests_llm.FastDeletePkRegressionTests.test_delete_clears_pk_for_models_with_inheritance_parent delete.tests_llm.FastDeletePkRegressionTests.test_fast_delete_single_instance_does_not_emit_pre_post_delete_signals delete.tests_llm.FastDeletePkRegressionTests.test_multiple_deletes_do_not_use_single_fast_path delete.tests_llm.FastDeletePkRegressionTests.test_queryset_delete_does_not_clear_instance_pk_on_returned_instances delete.tests_llm.FastDeletePkRegressionTests.test_single_instance_delete_return_dict_key_matches_label delete.tests_llm.FastDeletePkRegressionTests.test_single_instance_fast_delete_attname_is_same_as_pk_property delete.tests_llm.FastDeletePkRegressionTests.test_single_instance_fast_delete_clears_auto_pk delete.tests_llm.FastDeletePkRegressionTests.test_single_instance_fast_delete_clears_custom_pk_charfield delete.tests_llm.make_model
coverage json -o coverage.json
: '>>>>> End Test Output'
