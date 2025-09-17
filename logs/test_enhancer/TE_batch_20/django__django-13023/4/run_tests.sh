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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_decimalfield_llm.DecimalFieldRegressionTests.test_clean_accepts_tuple_representation model_fields.test_decimalfield_llm.DecimalFieldRegressionTests.test_clean_accepts_tuple_with_list_digits model_fields.test_decimalfield_llm.DecimalFieldRegressionTests.test_to_python_accepts_tuple_multiple_digits model_fields.test_decimalfield_llm.DecimalFieldRegressionTests.test_to_python_accepts_tuple_negative_sign model_fields.test_decimalfield_llm.DecimalFieldRegressionTests.test_to_python_accepts_tuple_representation_simple model_fields.test_decimalfield_llm.DecimalFieldRegressionTests.test_to_python_accepts_tuple_with_list_digits_inside
coverage json -o coverage.json
: '>>>>> End Test Output'
