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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityProgNameEdgeCasesTests.test_execute_from_command_line_prints_help_using_empty_prog_when_argv0_is_empty admin_scripts.tests_llm.ManagementUtilityProgNameEdgeCasesTests.test_execute_from_command_line_raises_typeerror_when_argv0_is_none admin_scripts.tests_llm.ManagementUtilityProgNameEdgeCasesTests.test_execute_prints_help_using_empty_prog_when_argv0_is_empty admin_scripts.tests_llm.ManagementUtilityProgNameEdgeCasesTests.test_init_raises_typeerror_when_argv0_is_none admin_scripts.tests_llm.ManagementUtilityProgNameEdgeCasesTests.test_main_help_text_contains_empty_prog_when_argv0_is_empty admin_scripts.tests_llm.ManagementUtilityProgNameEdgeCasesTests.test_multiple_execute_calls_with_empty_progname_remain_consistent admin_scripts.tests_llm.ManagementUtilityProgNameEdgeCasesTests.test_prog_name_empty_string_in_help_short_form admin_scripts.tests_llm.ManagementUtilityProgNameEdgeCasesTests.test_prog_name_empty_string_reflected_in_main_help_text_direct_call admin_scripts.tests_llm.ManagementUtilityProgNameEdgeCasesTests.test_prog_name_is_empty_string_when_argv0_is_empty admin_scripts.tests_llm.ManagementUtilityProgNameEdgeCasesTests.test_sys_argv_none_does_not_affect_execute_from_command_line_progname_resolution
coverage json -o coverage.json
: '>>>>> End Test Output'
