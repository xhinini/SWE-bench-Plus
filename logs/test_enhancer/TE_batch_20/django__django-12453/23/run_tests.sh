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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_check_constraints_called_even_with_multiple_objects backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_check_constraints_called_once_with_generator_deserialize backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_checks_disabled_called_on_creation_instance backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_checks_disabled_present_when_deserialize_is_lazy_iterator backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_context_entered_before_any_save_called backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_context_exited_after_saves_called backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_deserialize_works_when_no_objects_and_still_checks_constraints backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_uses_constraint_checks_disabled_and_calls_check_constraints_on_custom_connection backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_uses_constraint_checks_disabled_and_calls_check_constraints_on_default_connection
coverage json -o coverage.json
: '>>>>> End Test Output'
