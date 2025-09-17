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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ParserProgTests.test_execute_from_command_line_custom_progname_on_pythonpath_error admin_scripts.tests_llm.ParserProgTests.test_execute_from_command_line_relative_manage_py_shows_manage_py admin_scripts.tests_llm.ParserProgTests.test_execute_from_command_line_settings_missing_shows_given_prog admin_scripts.tests_llm.ParserProgTests.test_execute_from_command_line_shows_django_admin_prog_on_pythonpath_error admin_scripts.tests_llm.ParserProgTests.test_execute_from_command_line_shows_manage_py_basename_on_pythonpath_error admin_scripts.tests_llm.ParserProgTests.test_execute_from_command_line_shows_prog_for_missing_settings_arg admin_scripts.tests_llm.ParserProgTests.test_execute_from_command_line_shows_python_module_style_for___main__ admin_scripts.tests_llm.ParserProgTests.test_execute_from_command_line_shows_python_module_style_for_path_ending_in___main__ admin_scripts.tests_llm.ParserProgTests.test_management_utility_direct_empty_progname_results_in_blank_prog_in_usage admin_scripts.tests_llm.ParserProgTests.test_management_utility_direct_progname_shown_on_pythonpath_error
coverage json -o coverage.json
: '>>>>> End Test Output'
