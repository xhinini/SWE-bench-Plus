#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql_llm.test_accent_and_parameters dbshell.test_postgresql_llm.test_default_db_used_with_parameters dbshell.test_postgresql_llm.test_ipv6_and_colon_user_and_parameter dbshell.test_postgresql_llm.test_multiple_parameters_order dbshell.test_postgresql_llm.test_no_parameters_preserves_args dbshell.test_postgresql_llm.test_parameters_not_duplicated dbshell.test_postgresql_llm.test_parameters_position_with_user_host_port dbshell.test_postgresql_llm.test_parameters_with_service_and_passfile dbshell.test_postgresql_llm.test_passfile_and_parameters dbshell.test_postgresql_llm.test_service_preserves_no_db_and_parameters
coverage json -o coverage.json
: '>>>>> End Test Output'
