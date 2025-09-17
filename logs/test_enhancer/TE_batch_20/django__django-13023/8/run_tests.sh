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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_decimalfield_llm.DecimalFieldTupleInputTests.test_clean_accepts_decimal_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleInputTests.test_clean_does_not_reject_valid_tuple_input model_fields.test_decimalfield_llm.DecimalFieldTupleInputTests.test_get_db_prep_save_equivalence_negative_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleInputTests.test_get_db_prep_save_equivalence_with_decimal_and_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleInputTests.test_get_prep_value_accepts_decimal_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleInputTests.test_get_prep_value_accepts_namedtuple model_fields.test_decimalfield_llm.DecimalFieldTupleInputTests.test_namedtuple_decimal_like_is_accepted model_fields.test_decimalfield_llm.DecimalFieldTupleInputTests.test_to_python_accepts_decimal_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleInputTests.test_to_python_accepts_decimal_tuple_negative model_fields.test_decimalfield_llm.DecimalFieldTupleInputTests.test_tuple_subclass_decimal_like_is_accepted
coverage json -o coverage.json
: '>>>>> End Test Output'
