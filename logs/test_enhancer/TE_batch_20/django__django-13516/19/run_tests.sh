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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 user_commands.management.commands.test_outputwrapper_llm.DummyStreamWithFlush.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyStreamWithFlush.flush user_commands.management.commands.test_outputwrapper_llm.DummyStreamWithFlush.isatty user_commands.management.commands.test_outputwrapper_llm.DummyStreamWithFlush.write user_commands.management.commands.test_outputwrapper_llm.DummyStreamWithoutFlush.__init__ user_commands.management.commands.test_outputwrapper_llm.DummyStreamWithoutFlush.isatty user_commands.management.commands.test_outputwrapper_llm.DummyStreamWithoutFlush.write user_commands.management.commands.test_outputwrapper_llm.DummyStyle.ERROR user_commands.management.commands.test_outputwrapper_llm.DummyStyle.NOTICE user_commands.management.commands.test_outputwrapper_llm.DummyStyle.SQL_KEYWORD user_commands.management.commands.test_outputwrapper_llm.DummyStyle.WARNING user_commands.management.commands.test_outputwrapper_llm.DummyStyle.__call__ user_commands.management.commands.test_outputwrapper_llm.DummyStyle.__init__ user_commands.management.commands.test_outputwrapper_llm.MinimalCommand.__init__ user_commands.management.commands.test_outputwrapper_llm.MinimalCommand.handle
coverage json -o coverage.json
: '>>>>> End Test Output'
