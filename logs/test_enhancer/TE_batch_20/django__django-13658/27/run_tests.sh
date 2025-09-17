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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_execute_from_command_line_raises_typeerror_on_non_string_argv0_zero admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_execute_from_command_line_raises_typeerror_on_none_argv0 admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_execute_from_command_line_shows_empty_progname_in_usage admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_init_raises_typeerror_on_non_string_argv0_zero admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_init_raises_typeerror_on_none_argv0 admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_prog_name_is_empty_string_when_argv0_is_empty_string
coverage json -o coverage.json
: '>>>>> End Test Output'
