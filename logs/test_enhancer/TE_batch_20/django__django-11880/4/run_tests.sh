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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 forms_tests.tests.test_forms_llm.FormsTestCase.test_error_messages_deepcopy_shared_custom_object_charfield forms_tests.tests.test_forms_llm.FormsTestCase.test_error_messages_deepcopy_shared_custom_object_field forms_tests.tests.test_forms_llm.FormsTestCase.test_error_messages_deepcopy_shared_dict_value forms_tests.tests.test_forms_llm.FormsTestCase.test_error_messages_deepcopy_shared_list_value forms_tests.tests.test_forms_llm.FormsTestCase.test_error_messages_deepcopy_shared_mutation_visibility forms_tests.tests.test_forms_llm.FormsTestCase.test_error_messages_deepcopy_shared_on_choicefield forms_tests.tests.test_forms_llm.FormsTestCase.test_error_messages_deepcopy_shared_on_integerfield forms_tests.tests.test_forms_llm.FormsTestCase.test_error_messages_deepcopy_shared_on_multiplechoicefield forms_tests.tests.test_forms_llm.FormsTestCase.test_error_messages_deepcopy_shared_on_regexfield forms_tests.tests.test_forms_llm.FormsTestCase.test_error_messages_deepcopy_shared_set_value forms_tests.tests.test_forms_llm._make_custom
coverage json -o coverage.json
: '>>>>> End Test Output'
