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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_execute_from_command_line_argv0_false_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_execute_from_command_line_argv0_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_execute_from_command_line_argv0_zero_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_execute_help_subcommand_empty_prog_usage admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_execute_main_help_contains_empty_prog admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_init_argv0_false_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_init_argv0_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_init_argv0_zero_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_program_name_from_argv_unaffected
coverage json -o coverage.json
: '>>>>> End Test Output'
