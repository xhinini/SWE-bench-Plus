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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbFromStringExtra.test_check_constraints_called_empty backends.base.test_creation_llm.TestDeserializeDbFromStringExtra.test_check_constraints_called_once_with_multiple_objects backends.base.test_creation_llm.TestDeserializeDbFromStringExtra.test_check_constraints_called_with_objects backends.base.test_creation_llm.TestDeserializeDbFromStringExtra.test_constraint_checks_disabled_and_check_constraints_together backends.base.test_creation_llm.TestDeserializeDbFromStringExtra.test_constraint_checks_disabled_used_empty backends.base.test_creation_llm.TestDeserializeDbFromStringExtra.test_constraint_checks_disabled_used_with_objects backends.base.test_creation_llm.TestDeserializeDbFromStringExtra.test_forward_reference_deserialize
coverage json -o coverage.json
: '>>>>> End Test Output'
