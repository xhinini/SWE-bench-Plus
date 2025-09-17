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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.BadFlushStream.__init__ user_commands.management.commands.test_outputwrapper_llm.BadFlushStream.flush user_commands.management.commands.test_outputwrapper_llm.BadFlushStream.write user_commands.management.commands.test_outputwrapper_llm.CountingFlushStream.__init__ user_commands.management.commands.test_outputwrapper_llm.CountingFlushStream.flush user_commands.management.commands.test_outputwrapper_llm.CountingFlushStream.write user_commands.management.commands.test_outputwrapper_llm.NoFlushStream.__init__ user_commands.management.commands.test_outputwrapper_llm.NoFlushStream.write user_commands.management.commands.test_outputwrapper_llm.test_execute_replacing_stderr_with_stream_without_flush_does_not_raise user_commands.management.commands.test_outputwrapper_llm.test_flush_after_write_calls_underlying_flush_and_does_not_duplicate_writes user_commands.management.commands.test_outputwrapper_llm.test_flush_calls_underlying_flush user_commands.management.commands.test_outputwrapper_llm.test_flush_is_callable_on_wrapper_and_bound_to_wrapper_instance user_commands.management.commands.test_outputwrapper_llm.test_flush_no_underlying_flush_does_not_raise user_commands.management.commands.test_outputwrapper_llm.test_flush_on_stringio_works_and_is_bound_to_wrapper user_commands.management.commands.test_outputwrapper_llm.test_flush_propagates_exceptions_from_underlying_stream user_commands.management.commands.test_outputwrapper_llm.test_getattr_proxies_other_attributes_to_underlying_stream user_commands.management.commands.test_outputwrapper_llm.test_write_respects_ending_and_flush_does_not_append_an_extra_ending
coverage json -o coverage.json
: '>>>>> End Test Output'
