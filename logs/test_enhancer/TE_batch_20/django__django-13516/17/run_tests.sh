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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.DummyStream.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyStream.custom_method user_commands.management.commands.test_outputwrapper_llm.DummyStream.getvalue user_commands.management.commands.test_outputwrapper_llm.DummyStream.isatty user_commands.management.commands.test_outputwrapper_llm.DummyStream.write user_commands.management.commands.test_outputwrapper_llm.OutputWrapperTests.test_flush_noop_if_underlying_has_no_flush_attribute
coverage json -o coverage.json
: '>>>>> End Test Output'
