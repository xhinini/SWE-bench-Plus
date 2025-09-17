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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.DummyStream.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyStream.flush user_commands.management.commands.test_outputwrapper_llm.DummyStream.isatty user_commands.management.commands.test_outputwrapper_llm.DummyStream.marker user_commands.management.commands.test_outputwrapper_llm.DummyStream.write user_commands.management.commands.test_outputwrapper_llm.test___getattr___delegates_arbitrary_methods user_commands.management.commands.test_outputwrapper_llm.test_execute_no_color_sets_stderr_style_func_to_none_when_no_external_stderr user_commands.management.commands.test_outputwrapper_llm.test_execute_raises_when_both_no_color_and_force_color_are_true user_commands.management.commands.test_outputwrapper_llm.test_execute_writes_output_to_provided_stdout_and_returns_output user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_flush_no_attribute_no_error user_commands.management.commands.test_outputwrapper_llm.test_style_func_not_set_if_not_isatty user_commands.management.commands.test_outputwrapper_llm.test_style_func_set_only_if_isatty_true user_commands.management.commands.test_outputwrapper_llm.test_write_appends_ending_but_not_duplicate user_commands.management.commands.test_outputwrapper_llm.test_write_style_func_parameter_overrides_property
coverage json -o coverage.json
: '>>>>> End Test Output'
