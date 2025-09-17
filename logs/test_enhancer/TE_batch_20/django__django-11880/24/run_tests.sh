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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_custom_object_charfield forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_list_of_custom_objects_charfield forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_mutable_dict_charfield forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_mutable_list_charfield forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_mutable_value_in_booleanfield forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_mutable_value_in_choicefield forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_mutable_value_in_filefield forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_mutable_value_in_imagefield forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_mutable_value_in_integerfield forms_tests.tests.test_forms_llm.test_field_deepcopy_shares_nested_mutable_structure_charfield
coverage json -o coverage.json
: '>>>>> End Test Output'
