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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityProgramNameTests._run_and_get_stdout admin_scripts.tests_llm.ManagementUtilityProgramNameTests.test_django_admin_long_help_shows_django_admin admin_scripts.tests_llm.ManagementUtilityProgramNameTests.test_django_admin_with_absolute_path_shows_basename admin_scripts.tests_llm.ManagementUtilityProgramNameTests.test_manage_py_help_when_argv0_is_empty_string_uses_basename_behavior admin_scripts.tests_llm.ManagementUtilityProgramNameTests.test_manage_py_long_help_shows_manage_py admin_scripts.tests_llm.ManagementUtilityProgramNameTests.test_manage_py_short_help_shows_manage_py admin_scripts.tests_llm.ManagementUtilityProgramNameTests.test_manage_py_with_path_shows_basename
coverage json -o coverage.json
: '>>>>> End Test Output'
