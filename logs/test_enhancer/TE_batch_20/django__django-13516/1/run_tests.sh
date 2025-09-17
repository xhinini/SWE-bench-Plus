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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.DummyStream.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyStream.flush user_commands.management.commands.test_outputwrapper_llm.DummyStream.getvalue user_commands.management.commands.test_outputwrapper_llm.DummyStream.isatty user_commands.management.commands.test_outputwrapper_llm.DummyStream.write user_commands.management.commands.test_outputwrapper_llm.test_basecommand_execute_uses_provided_stdout_and_stderr_wrappers user_commands.management.commands.test_outputwrapper_llm.test_basecommand_execute_with_no_color_disables_stderr_style_func user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_flush_does_not_raise_if_underlying_has_no_flush user_commands.management.commands.test_outputwrapper_llm.test_isatty_reflects_underlying_isatty user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_respects_isatty user_commands.management.commands.test_outputwrapper_llm.test_write_appends_ending_when_missing user_commands.management.commands.test_outputwrapper_llm.test_write_preserves_message_if_endswith_ending user_commands.management.commands.test_outputwrapper_llm.test_write_uses_style_func_argument_to_override_property user_commands.management.commands.test_outputwrapper_llm.test_write_uses_style_func_property_if_no_arg_passed
coverage json -o coverage.json
: '>>>>> End Test Output'
