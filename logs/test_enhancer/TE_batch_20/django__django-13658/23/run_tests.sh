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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityInitTests.test_execute_from_command_line_with_empty_progname_in_argv admin_scripts.tests_llm.ManagementUtilityInitTests.test_init_raises_indexerror_on_empty_argv_list admin_scripts.tests_llm.ManagementUtilityInitTests.test_init_raises_typeerror_on_none_argv0 admin_scripts.tests_llm.ManagementUtilityInitTests.test_main_help_text_includes_empty_prog_placeholder admin_scripts.tests_llm.ManagementUtilityInitTests.test_prog_name_is_empty_string_when_argv0_empty admin_scripts.tests_llm.ManagementUtilityInitTests.test_prog_name_preserved_for_paths_with_backslashes admin_scripts.tests_llm.ManagementUtilityInitTests.test_prog_name_special_case_main_module admin_scripts.tests_llm.ManagementUtilityInitTests.test_prog_name_uses_basename_of_argv0
coverage json -o coverage.json
: '>>>>> End Test Output'
