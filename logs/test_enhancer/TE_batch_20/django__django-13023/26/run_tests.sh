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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_clean_accepts_decimal_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_clean_with_max_digits_allows_valid_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_clean_with_tuple_exceeding_whole_digits_raises model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_get_db_prep_save_accepts_decimal_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_get_db_prep_value_accepts_decimal_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_get_prep_value_accepts_decimal_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_negative_value_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_to_python_accepts_decimal_tuple model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_to_python_preserves_exact_tuple_value model_fields.test_decimalfield_llm.DecimalFieldTupleTests.test_tuple_zero_exponent
coverage json -o coverage.json
: '>>>>> End Test Output'
