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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_autocomplete_path_raises_with_none_argv0 admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_execute_from_command_line_raises_with_list_none admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_execute_from_command_line_raises_with_tuple_none admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_execute_method_invocation_raises_with_none_argv0 admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_fetch_command_raises_with_none_argv0 admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_instantiation_raises_typeerror_with_list_none admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_instantiation_raises_typeerror_with_list_none_and_help admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_instantiation_raises_typeerror_with_tuple_none admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_instantiation_raises_typeerror_with_tuple_none_and_help admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_main_help_text_access_raises_with_none_argv0
coverage json -o coverage.json
: '>>>>> End Test Output'
