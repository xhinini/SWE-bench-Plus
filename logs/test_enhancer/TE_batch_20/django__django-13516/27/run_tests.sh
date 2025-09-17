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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.FakeStreamNoFlush.__init__ user_commands.management.commands.test_outputwrapper_llm.FakeStreamNoFlush.isatty user_commands.management.commands.test_outputwrapper_llm.FakeStreamNoFlush.write user_commands.management.commands.test_outputwrapper_llm.FakeStreamWithFlush.__init__ user_commands.management.commands.test_outputwrapper_llm.FakeStreamWithFlush.flush user_commands.management.commands.test_outputwrapper_llm.FakeStreamWithFlush.isatty user_commands.management.commands.test_outputwrapper_llm.FakeStreamWithFlush.write user_commands.management.commands.test_outputwrapper_llm.test_basecommand_execute_writes_output_to_provided_stdout_and_stderr_wrapping user_commands.management.commands.test_outputwrapper_llm.test_execute_color_option_conflict_raises user_commands.management.commands.test_outputwrapper_llm.test_execute_no_color_sets_stderr_style_func_to_none user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_flush_no_underlying_flush_no_error user_commands.management.commands.test_outputwrapper_llm.test_outputwrapper_write_adds_ending_if_missing user_commands.management.commands.test_outputwrapper_llm.test_outputwrapper_write_preserves_existing_ending user_commands.management.commands.test_outputwrapper_llm.test_setting_style_func_to_none_uses_identity user_commands.management.commands.test_outputwrapper_llm.test_style_func_applied_only_when_isatty_true
coverage json -o coverage.json
: '>>>>> End Test Output'
