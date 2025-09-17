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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_decimalfield_llm.DecimalFieldTupleTests.setUp model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_clean_accepts_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_clean_tuple_preserves_scale model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_get_prep_value_accepts_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_to_python_namedtuple model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_to_python_tuple_basic model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_to_python_tuple_large_digits model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_to_python_tuple_many_digits model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_to_python_tuple_negative model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_to_python_tuple_single_digit model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_to_python_tuple_zero_exponent
coverage json -o coverage.json
: '>>>>> End Test Output'
