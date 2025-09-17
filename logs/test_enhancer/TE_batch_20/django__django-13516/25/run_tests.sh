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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.DummyStreamNoFlush.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyStreamNoFlush.isatty user_commands.management.commands.test_outputwrapper_llm.DummyStreamNoFlush.write user_commands.management.commands.test_outputwrapper_llm.DummyStreamWithFlush.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyStreamWithFlush.flush user_commands.management.commands.test_outputwrapper_llm.DummyStreamWithFlush.isatty user_commands.management.commands.test_outputwrapper_llm.DummyStreamWithFlush.write user_commands.management.commands.test_outputwrapper_llm.test___getattr___forwards_attributes_to_underlying_stream user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush_when_present user_commands.management.commands.test_outputwrapper_llm.test_flush_is_noop_when_underlying_has_no_flush user_commands.management.commands.test_outputwrapper_llm.test_isatty_proxies_to_underlying_stream user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_ignores_style_when_underlying_not_isatty user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_uses_underlying_isatty_true user_commands.management.commands.test_outputwrapper_llm.test_write_appends_configured_ending_if_missing user_commands.management.commands.test_outputwrapper_llm.test_write_does_not_append_ending_if_already_present user_commands.management.commands.test_outputwrapper_llm.test_write_respects_provided_style_func_over_wrapper_style user_commands.management.commands.test_outputwrapper_llm.test_write_with_ending_none_does_not_append_ending
coverage json -o coverage.json
: '>>>>> End Test Output'
