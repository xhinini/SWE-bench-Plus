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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.setUp model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_clean_accepts_dict_subclass_with_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_clean_accepts_list_subclass_with_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_clean_accepts_list_subclass_with_whitespace_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_clean_accepts_set_subclass_with_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_clean_accepts_tuple_subclass_with_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_to_python_accepts_dict_subclass_with_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_to_python_accepts_list_subclass_with_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_to_python_accepts_set_subclass_with_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_to_python_accepts_tuple_subclass_with_str model_fields.test_decimalfield_llm.DecimalFieldContainerSubclassTests.test_to_python_str_with_whitespace model_fields.test_decimalfield_llm.DictLike.__str__ model_fields.test_decimalfield_llm.ListLike.__str__ model_fields.test_decimalfield_llm.ListLikeSpaces.__str__ model_fields.test_decimalfield_llm.SetLike.__str__ model_fields.test_decimalfield_llm.TupleLike.__str__
coverage json -o coverage.json
: '>>>>> End Test Output'
