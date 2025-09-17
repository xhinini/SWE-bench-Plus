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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityEdgeCases.test_execute_from_command_line_with_argv0_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityEdgeCases.test_execute_from_command_line_with_argv0_zero_raises_typeerror admin_scripts.tests_llm.ManagementUtilityEdgeCases.test_execute_from_command_line_with_empty_list_raises_indexerror admin_scripts.tests_llm.ManagementUtilityEdgeCases.test_execute_from_command_line_with_empty_progname_prints_help admin_scripts.tests_llm.ManagementUtilityEdgeCases.test_init_with_argv0_false_raises_typeerror admin_scripts.tests_llm.ManagementUtilityEdgeCases.test_init_with_argv0_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityEdgeCases.test_init_with_argv0_zero_raises_typeerror admin_scripts.tests_llm.ManagementUtilityEdgeCases.test_init_with_empty_argv_raises_indexerror admin_scripts.tests_llm.ManagementUtilityEdgeCases.test_main_help_text_uses_empty_progname admin_scripts.tests_llm.ManagementUtilityEdgeCases.test_prog_name_is_empty_string_when_argv0_is_empty_string
coverage json -o coverage.json
: '>>>>> End Test Output'
