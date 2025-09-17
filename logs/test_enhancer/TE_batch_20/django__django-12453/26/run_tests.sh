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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_constraint_checks_disabled_used backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_deserialize_calls_check_constraints backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_deserialize_empty_list backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_deserialize_rolls_back_on_save_error backends.base.test_creation_llm.TestDeserializeDbFromStringAdditional.test_deserialize_with_whitespace
coverage json -o coverage.json
: '>>>>> End Test Output'
