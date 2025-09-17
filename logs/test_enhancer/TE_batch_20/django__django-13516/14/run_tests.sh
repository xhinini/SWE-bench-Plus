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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.DummyStream.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyStream.flush user_commands.management.commands.test_outputwrapper_llm.DummyStream.isatty user_commands.management.commands.test_outputwrapper_llm.DummyStream.write user_commands.management.commands.test_outputwrapper_llm.test_basecommand_execute_disables_stderr_color_with_no_color_option user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_flush_noop_if_no_flush_attribute user_commands.management.commands.test_outputwrapper_llm.test_flush_propagates_exception_from_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_isatty_reflects_underlying_stream user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_with_non_tty_disables_style user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_with_tty_enables_style user_commands.management.commands.test_outputwrapper_llm.test_write_adds_ending_when_missing user_commands.management.commands.test_outputwrapper_llm.test_write_does_not_duplicate_ending_when_present user_commands.management.commands.test_outputwrapper_llm.test_write_uses_passed_style_func_over_wrapper_style
coverage json -o coverage.json
: '>>>>> End Test Output'
