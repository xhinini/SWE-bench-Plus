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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling._make_cm backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling._make_deserialize backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling._make_obj backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling.test_deserialize_constraints_with_eight_objects backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling.test_deserialize_constraints_with_five_objects backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling.test_deserialize_constraints_with_four_objects backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling.test_deserialize_constraints_with_nine_objects backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling.test_deserialize_constraints_with_no_objects backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling.test_deserialize_constraints_with_one_object backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling.test_deserialize_constraints_with_seven_objects backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling.test_deserialize_constraints_with_six_objects backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling.test_deserialize_constraints_with_three_objects backends.base.test_creation_llm.TestDeserializeDbFromStringConstraintHandling.test_deserialize_constraints_with_two_objects
coverage json -o coverage.json
: '>>>>> End Test Output'
