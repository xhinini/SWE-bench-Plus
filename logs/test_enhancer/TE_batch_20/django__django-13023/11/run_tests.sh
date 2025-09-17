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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.setUp model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_dict_subclass_with_negative_number model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_dict_subclass_with_numeric_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_list_subclass_with_nan model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_list_subclass_with_numeric_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_list_subclass_with_whitespace_numeric_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_set_subclass_with_numeric_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_set_subclass_with_plus_sign model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_tuple_subclass_with_exponent_notation model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_tuple_subclass_with_large_decimal model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_tuple_subclass_with_numeric_str
coverage json -o coverage.json
: '>>>>> End Test Output'
