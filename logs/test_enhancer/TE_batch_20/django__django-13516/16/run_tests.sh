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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.DummyStream.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyStream.fileno user_commands.management.commands.test_outputwrapper_llm.DummyStream.flush user_commands.management.commands.test_outputwrapper_llm.DummyStream.isatty user_commands.management.commands.test_outputwrapper_llm.DummyStream.write user_commands.management.commands.test_outputwrapper_llm.NoFlushStream.__init__ user_commands.management.commands.test_outputwrapper_llm.NoFlushStream.isatty user_commands.management.commands.test_outputwrapper_llm.NoFlushStream.write user_commands.management.commands.test_outputwrapper_llm.RaisingFlushStream.flush user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush_when_available user_commands.management.commands.test_outputwrapper_llm.test_flush_no_error_when_no_flush_attr user_commands.management.commands.test_outputwrapper_llm.test_flush_propagates_exception_from_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_getattr_delegates_to_underlying_stream user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_sets_to_identity_when_not_tty user_commands.management.commands.test_outputwrapper_llm.test_write_appends_default_ending user_commands.management.commands.test_outputwrapper_llm.test_write_does_not_duplicate_ending_if_already_present user_commands.management.commands.test_outputwrapper_llm.test_write_uses_style_func_argument_over_wrapper_default user_commands.management.commands.test_outputwrapper_llm.test_write_uses_wrapper_style_func_when_no_arg user_commands.management.commands.test_outputwrapper_llm.test_write_with_custom_ending
coverage json -o coverage.json
: '>>>>> End Test Output'
