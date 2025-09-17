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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityProgramNameEdgeCases.test_execute_from_command_line_empty_progname_and_subcommand_help admin_scripts.tests_llm.ManagementUtilityProgramNameEdgeCases.test_execute_from_command_line_empty_progname_main_help_text_type_line admin_scripts.tests_llm.ManagementUtilityProgramNameEdgeCases.test_execute_from_command_line_empty_progname_usage_for_shell admin_scripts.tests_llm.ManagementUtilityProgramNameEdgeCases.test_execute_from_command_line_empty_progname_with_help_flag admin_scripts.tests_llm.ManagementUtilityProgramNameEdgeCases.test_execute_from_command_line_raises_when_sys_argv0_is_none admin_scripts.tests_llm.ManagementUtilityProgramNameEdgeCases.test_execute_from_command_line_with_sys_argv_none_and_help_flag admin_scripts.tests_llm.ManagementUtilityProgramNameEdgeCases.test_management_utility_init_raises_when_sys_argv0_is_none admin_scripts.tests_llm.ManagementUtilityProgramNameEdgeCases.test_management_utility_init_with_none_and_additional_args_raises
coverage json -o coverage.json
: '>>>>> End Test Output'
