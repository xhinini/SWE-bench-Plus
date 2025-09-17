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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.DummyStream.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyStream._do_flush user_commands.management.commands.test_outputwrapper_llm.DummyStream.isatty user_commands.management.commands.test_outputwrapper_llm.DummyStream.write user_commands.management.commands.test_outputwrapper_llm.test_basecommand_execute_writes_handle_output_to_stdout_and_flushable user_commands.management.commands.test_outputwrapper_llm.test_basecommand_init_raises_if_no_color_and_force_color user_commands.management.commands.test_outputwrapper_llm.test_execute_raises_if_force_and_no_color_options_together user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush_if_present user_commands.management.commands.test_outputwrapper_llm.test_flush_no_error_if_underlying_has_no_flush user_commands.management.commands.test_outputwrapper_llm.test_isatty_and_getattr_proxy_to_underlying_stream user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_uses_isatty_to_determine_storage user_commands.management.commands.test_outputwrapper_llm.test_write_appends_ending_when_missing_and_respects_existing_ending user_commands.management.commands.test_outputwrapper_llm.test_write_uses_style_func_property_and_argument_override
coverage json -o coverage.json
: '>>>>> End Test Output'
