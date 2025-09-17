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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_execute_from_command_line_prefers_passed_argv_over_sys_argv admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_execute_from_command_line_uses_empty_progname admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_execute_from_command_line_with_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_execute_prints_help_with_empty_progname admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_execute_uses_empty_progname_even_if_sys_argv_differs admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_main_help_text_commands_only_does_not_include_progname admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_main_help_text_includes_empty_progname admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_managementutility_init_with_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_prog_name_attribute_empty_string admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_prog_name_is_python_m_module_for_main_py
coverage json -o coverage.json
: '>>>>> End Test Output'
