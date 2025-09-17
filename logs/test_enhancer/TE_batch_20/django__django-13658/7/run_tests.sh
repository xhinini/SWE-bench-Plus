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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_help_uses_prog_name_for_empty_string_argv admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_help_when_progname_empty_via_execute_from_command_line admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_init_raises_typeerror_with_none_argv0
coverage json -o coverage.json
: '>>>>> End Test Output'
