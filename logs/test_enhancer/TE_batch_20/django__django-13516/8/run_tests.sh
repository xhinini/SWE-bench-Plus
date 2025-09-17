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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.test___getattr_forwards_methods user_commands.management.commands.test_outputwrapper_llm.test_execute_wraps_output_in_transaction_when_requested user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_flush_no_error_when_no_flush user_commands.management.commands.test_outputwrapper_llm.test_run_from_argv_handles_CommandError_without_traceback user_commands.management.commands.test_outputwrapper_llm.test_style_func_set_to_none_disables_styling user_commands.management.commands.test_outputwrapper_llm.test_style_func_setter_honors_isatty user_commands.management.commands.test_outputwrapper_llm.test_write_appends_ending user_commands.management.commands.test_outputwrapper_llm.test_write_respects_explicit_ending user_commands.management.commands.test_outputwrapper_llm.test_write_uses_passed_style_func
coverage json -o coverage.json
: '>>>>> End Test Output'
