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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 view_tests.tests.test_debug_llm.CleanseSettingSequenceSubclassTests.setUp view_tests.tests.test_debug_llm.CleanseSettingSequenceSubclassTests.test_badlist_does_not_preserve_type view_tests.tests.test_debug_llm.CleanseSettingSequenceSubclassTests.test_badtuple_does_not_preserve_type view_tests.tests.test_debug_llm.CleanseSettingSequenceSubclassTests.test_list_subclass_callable_wrapping view_tests.tests.test_debug_llm.CleanseSettingSequenceSubclassTests.test_list_subclass_empty view_tests.tests.test_debug_llm.CleanseSettingSequenceSubclassTests.test_list_subclass_nested_in_dict view_tests.tests.test_debug_llm.CleanseSettingSequenceSubclassTests.test_list_subclass_top_level view_tests.tests.test_debug_llm.CleanseSettingSequenceSubclassTests.test_mixed_nested_badlist_and_badtuple view_tests.tests.test_debug_llm.CleanseSettingSequenceSubclassTests.test_tuple_subclass_callable_wrapping view_tests.tests.test_debug_llm.CleanseSettingSequenceSubclassTests.test_tuple_subclass_nested_in_dict view_tests.tests.test_debug_llm.CleanseSettingSequenceSubclassTests.test_tuple_subclass_top_level
coverage json -o coverage.json
: '>>>>> End Test Output'
