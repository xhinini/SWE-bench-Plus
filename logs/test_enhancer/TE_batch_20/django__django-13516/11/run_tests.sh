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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.test_basecommand_execute_conflict_and_writes_output user_commands.management.commands.test_outputwrapper_llm.test_basecommand_init_conflicting_color_flags user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_flush_is_noop_if_no_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_getattr_forwards_to_underlying user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_respects_isatty user_commands.management.commands.test_outputwrapper_llm.test_write_appends_default_ending user_commands.management.commands.test_outputwrapper_llm.test_write_custom_ending user_commands.management.commands.test_outputwrapper_llm.test_write_no_duplicate_ending user_commands.management.commands.test_outputwrapper_llm.test_write_uses_provided_style_func_over_wrapper_style
coverage json -o coverage.json
: '>>>>> End Test Output'
