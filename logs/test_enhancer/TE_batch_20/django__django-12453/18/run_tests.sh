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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_called_after_all_saves backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_called_on_circular_reference_data backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_called_on_empty_data backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_disabled_before_saving_multiple_objects backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_disabled_before_saving_single_object backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_disabled_called_each_time_deserialize_invoked backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_disabled_used_when_alias_non_default backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_disabled_with_separate_connection_copy backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_deserialize_calls_check_constraints_once_even_with_generator backends.base.test_creation_llm.get_connection_copy_for_tests
coverage json -o coverage.json
: '>>>>> End Test Output'
