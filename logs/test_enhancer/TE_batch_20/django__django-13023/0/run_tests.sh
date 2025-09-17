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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_decimalfield_llm.DecimalFieldTupleConversionTests.test_to_python_accepts_decimal_as_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleConversionTests.test_to_python_accepts_negative_decimal_as_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleConversionTests.test_to_python_accepts_negative_large_exponent_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleConversionTests.test_to_python_accepts_negative_sign_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleConversionTests.test_to_python_accepts_positive_exponent_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleConversionTests.test_to_python_accepts_simple_decimal_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleConversionTests.test_to_python_accepts_subclassed_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleConversionTests.test_to_python_accepts_various_digits_and_exponent model_fields.test_decimalfield_llm.DecimalFieldTupleConversionTests.test_to_python_accepts_zero_exponent_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleConversionTests.test_to_python_accepts_zero_tuple
coverage json -o coverage.json
: '>>>>> End Test Output'
