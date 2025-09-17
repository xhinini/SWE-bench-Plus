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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.DummyOutNoFlush.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyOutNoFlush.isatty user_commands.management.commands.test_outputwrapper_llm.DummyOutNoFlush.write user_commands.management.commands.test_outputwrapper_llm.DummyOutWithFlush.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyOutWithFlush.flush user_commands.management.commands.test_outputwrapper_llm.DummyOutWithFlush.isatty user_commands.management.commands.test_outputwrapper_llm.DummyOutWithFlush.write user_commands.management.commands.test_outputwrapper_llm.test___getattr___delegates_other_attributes_to_underlying user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_flush_is_noop_if_underlying_has_no_flush user_commands.management.commands.test_outputwrapper_llm.test_isatty_delegates_to_underlying_stream user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_and_getter_when_tty_true user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_sets_identity_when_not_tty_or_none user_commands.management.commands.test_outputwrapper_llm.test_write_appends_default_ending_once user_commands.management.commands.test_outputwrapper_llm.test_write_preserves_style_func_property_when_no_style_arg_passed user_commands.management.commands.test_outputwrapper_llm.test_write_respects_custom_ending_and_no_duplicate user_commands.management.commands.test_outputwrapper_llm.test_write_uses_given_style_func_argument_over_default
coverage json -o coverage.json
: '>>>>> End Test Output'
