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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_execute_from_command_line_with_argv0_none_and_more_args_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_execute_from_command_line_with_argv0_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_execute_from_command_line_with_only_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_init_with_argv0_none_and_subcommand_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_init_with_argv0_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_instantiation_then_autocomplete_with_argv0_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_instantiation_with_none_and_empty_string_following_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_main_help_text_construction_with_argv0_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_managementutility_execute_with_argv0_none_raises_typeerror admin_scripts.tests_llm.ManagementUtilityArgvNoneTests.test_multiple_none_and_values_in_argv_raises_typeerror
coverage json -o coverage.json
: '>>>>> End Test Output'
