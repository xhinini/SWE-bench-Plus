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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbFromStringRegression._make_connection_with_cm backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_called_once_with_many_objects backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_not_called_on_exception_during_save backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_disabled_and_check_constraints_called backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_disabled_and_check_constraints_called_no_objects backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_disabled_and_check_constraints_called_with_stream_obj backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_disabled_called_once backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_context_manager_enter_exception_propagates backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_deserialize_called_with_using_and_format backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_deserialize_handles_unicode_string_and_checks_constraints backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_multiple_objects_order_saved
coverage json -o coverage.json
: '>>>>> End Test Output'
