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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_execute_from_command_line_with_empty_prog_in_argv_displays_blank_prog_in_usage admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_execute_from_command_line_with_explicit_empty_prog_and_help_outputs_blank_usage admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_init_none_uses_sysargv_with_empty_string_sets_prog_name_empty admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_init_none_uses_sysargv_with_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_init_with_argv_starting_with_empty_string_sets_prog_name_empty admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_init_with_argv_starting_with_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvEdgeCasesTests.test_managementutility_explicit_empty_string_in_argv_results_in_blank_prog
coverage json -o coverage.json
: '>>>>> End Test Output'
