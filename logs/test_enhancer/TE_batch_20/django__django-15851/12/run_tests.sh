#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.test_ipv6_host_and_parameters_with_default_db dbshell.test_postgresql_llm.test_parameters_default_db_when_name_missing dbshell.test_postgresql_llm.test_parameters_default_db_with_empty_name dbshell.test_postgresql_llm.test_parameters_default_db_with_none_name dbshell.test_postgresql_llm.test_parameters_multiple_args_before_db dbshell.test_postgresql_llm.test_parameters_with_host_port_and_default_db dbshell.test_postgresql_llm.test_parameters_with_service_and_parameters dbshell.test_postgresql_llm.test_parameters_with_service_and_passfile_and_parameters dbshell.test_postgresql_llm.test_port_as_int_and_parameters dbshell.test_postgresql_llm.test_user_and_parameters_with_missing_db
coverage json -o coverage.json
: '>>>>> End Test Output'
