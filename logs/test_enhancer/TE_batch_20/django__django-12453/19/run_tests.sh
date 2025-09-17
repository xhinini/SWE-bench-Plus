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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbFromStringRegression._install_wrappers backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_atomic_enter_exit_called_each_time backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_called_multiple_times backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_check_constraints_called_on_empty_data backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_checks_and_check_constraints_called backends.base.test_creation_llm.TestDeserializeDbFromStringRegression.test_constraint_enter_exit_and_check_constraints_sequence
coverage json -o coverage.json
: '>>>>> End Test Output'
