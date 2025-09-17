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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ProgramNameHelpTests.test_execute_from_command_line_help_flag_with_empty_prog admin_scripts.tests_llm.ProgramNameHelpTests.test_execute_from_command_line_with_empty_prog_shows_empty_prog_in_usage admin_scripts.tests_llm.ProgramNameHelpTests.test_managementutility_main_help_text_uses_empty_prog
coverage json -o coverage.json
: '>>>>> End Test Output'
