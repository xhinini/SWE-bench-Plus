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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityArgvFalsyTests.test_execute_from_command_line_raises_typeerror_on_false_argv0 admin_scripts.tests_llm.ManagementUtilityArgvFalsyTests.test_execute_from_command_line_raises_typeerror_on_int_zero_argv0 admin_scripts.tests_llm.ManagementUtilityArgvFalsyTests.test_execute_from_command_line_raises_typeerror_when_sys_argv0_is_none admin_scripts.tests_llm.ManagementUtilityArgvFalsyTests.test_execute_from_command_line_reflects_empty_progname_in_usage admin_scripts.tests_llm.ManagementUtilityArgvFalsyTests.test_init_raises_typeerror_on_false_argv0 admin_scripts.tests_llm.ManagementUtilityArgvFalsyTests.test_init_raises_typeerror_on_none_argv0 admin_scripts.tests_llm.ManagementUtilityArgvFalsyTests.test_init_raises_typeerror_on_zero_argv0 admin_scripts.tests_llm.ManagementUtilityArgvFalsyTests.test_main_help_text_shows_empty_progname_type_line admin_scripts.tests_llm.ManagementUtilityArgvFalsyTests.test_no_argv_uses_sys_argv_and_raises_if_sys_argv0_is_none admin_scripts.tests_llm.ManagementUtilityArgvFalsyTests.test_prog_name_is_empty_string_when_argv0_is_empty_string
coverage json -o coverage.json
: '>>>>> End Test Output'
