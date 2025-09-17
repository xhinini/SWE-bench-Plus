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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_main_help_text_commands_only_true_returns_commands_list admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_main_help_text_contains_empty_prog_placeholder admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_main_help_text_empty_prog_and_app_section admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_main_help_text_shows_program_name_for_non_empty admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_prog_name_basename admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_prog_name_empty_string_property admin_scripts.tests_llm.ManagementUtilityProgNameTests.test_prog_name_python_m_main
coverage json -o coverage.json
: '>>>>> End Test Output'
