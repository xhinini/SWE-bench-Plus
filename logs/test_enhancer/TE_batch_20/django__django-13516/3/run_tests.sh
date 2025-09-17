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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.DummyIsattyFalse.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyIsattyFalse.isatty user_commands.management.commands.test_outputwrapper_llm.DummyIsattyFalse.write user_commands.management.commands.test_outputwrapper_llm.DummyIsattyTrue.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyIsattyTrue.flush user_commands.management.commands.test_outputwrapper_llm.DummyIsattyTrue.isatty user_commands.management.commands.test_outputwrapper_llm.DummyIsattyTrue.write user_commands.management.commands.test_outputwrapper_llm.DummyNoFlush.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyNoFlush.write user_commands.management.commands.test_outputwrapper_llm.DummyWithFlush.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyWithFlush.flush user_commands.management.commands.test_outputwrapper_llm.test___getattr___proxies_other_attributes user_commands.management.commands.test_outputwrapper_llm.test_basecommand_init_conflicting_color_flags_raises user_commands.management.commands.test_outputwrapper_llm.test_basecommand_sets_stderr_style_when_color_enabled user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_flush_with_no_underlying_flush_does_not_error user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_respects_isatty user_commands.management.commands.test_outputwrapper_llm.test_write_appends_ending_once user_commands.management.commands.test_outputwrapper_llm.test_write_preserves_existing_ending_and_does_not_duplicate user_commands.management.commands.test_outputwrapper_llm.test_write_uses_explicit_style_func_argument_over_property
coverage json -o coverage.json
: '>>>>> End Test Output'
