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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_decimalfield_llm.DecimalFieldRegressionTests.test_bytes_numeric_is_accepted model_fields.test_decimalfield_llm.DecimalFieldRegressionTests.test_float_conversion_and_rounding_behavior_is_preserved model_fields.test_decimalfield_llm.DecimalFieldRegressionTests.test_numeric_subclass_dict_is_converted_to_decimal model_fields.test_decimalfield_llm.DecimalFieldRegressionTests.test_numeric_subclass_list_is_converted_to_decimal model_fields.test_decimalfield_llm.DecimalFieldRegressionTests.test_numeric_subclass_set_is_converted_to_decimal model_fields.test_decimalfield_llm.DecimalFieldRegressionTests.test_numeric_subclass_tuple_is_converted_to_decimal
coverage json -o coverage.json
: '>>>>> End Test Output'
