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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeConstraintHandling._make_cm backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_check_constraints_called_after_saves backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_check_constraints_called_when_serializer_is_generator backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_checks_disabled_called backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_checks_disabled_called_on_copy_connection backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_constraint_context_manager_used_before_any_save backends.base.test_creation_llm.TestDeserializeConstraintHandling.test_no_objects_still_calls_constraint_checks
coverage json -o coverage.json
: '>>>>> End Test Output'
