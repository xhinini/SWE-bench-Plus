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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.FakeStreamNoFlush.__init__ user_commands.management.commands.test_outputwrapper_llm.FakeStreamNoFlush.getvalue user_commands.management.commands.test_outputwrapper_llm.FakeStreamNoFlush.isatty user_commands.management.commands.test_outputwrapper_llm.FakeStreamNoFlush.write user_commands.management.commands.test_outputwrapper_llm.FakeStreamWithFlush.__init__ user_commands.management.commands.test_outputwrapper_llm.FakeStreamWithFlush.flush user_commands.management.commands.test_outputwrapper_llm.FakeStreamWithFlush.getvalue user_commands.management.commands.test_outputwrapper_llm.FakeStreamWithFlush.isatty user_commands.management.commands.test_outputwrapper_llm.FakeStreamWithFlush.write user_commands.management.commands.test_outputwrapper_llm.test___getattr__delegates_other_methods_to_underlying_stream user_commands.management.commands.test_outputwrapper_llm.test_basecommand_execute_writes_handle_output_to_stdout_wrapper user_commands.management.commands.test_outputwrapper_llm.test_execute_assigns_stdout_and_stderr_from_options_and_uses_wrappers user_commands.management.commands.test_outputwrapper_llm.test_execute_no_color_and_force_color_conflict_raises_CommandError user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush_if_present user_commands.management.commands.test_outputwrapper_llm.test_flush_does_not_raise_if_underlying_lacks_flush user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_uses_isatty_to_enable_or_disable user_commands.management.commands.test_outputwrapper_llm.test_write_adds_ending_when_missing user_commands.management.commands.test_outputwrapper_llm.test_write_applies_passed_style_func_over_default user_commands.management.commands.test_outputwrapper_llm.test_write_does_not_duplicate_ending
coverage json -o coverage.json
: '>>>>> End Test Output'
