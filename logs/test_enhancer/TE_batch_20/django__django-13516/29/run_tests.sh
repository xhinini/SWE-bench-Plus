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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.DummyStream.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyStream.flush user_commands.management.commands.test_outputwrapper_llm.DummyStream.isatty user_commands.management.commands.test_outputwrapper_llm.NoFlushStream.isatty user_commands.management.commands.test_outputwrapper_llm.test_basecommand_execute_uses_provided_stdout_and_stderr_wrappers user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_flush_does_not_error_if_underlying_has_no_flush user_commands.management.commands.test_outputwrapper_llm.test_isatty_delegates_to_underlying_stream user_commands.management.commands.test_outputwrapper_llm.test_outputwrapper_write_with_style_func_parameter_overrides_instance_style user_commands.management.commands.test_outputwrapper_llm.test_run_from_argv_handles_commanderror_and_exits_without_traceback user_commands.management.commands.test_outputwrapper_llm.test_style_func_applied_when_tty_true user_commands.management.commands.test_outputwrapper_llm.test_style_func_not_applied_when_not_tty user_commands.management.commands.test_outputwrapper_llm.test_write_appends_default_ending user_commands.management.commands.test_outputwrapper_llm.test_write_respects_explicit_ending_argument
coverage json -o coverage.json
: '>>>>> End Test Output'
