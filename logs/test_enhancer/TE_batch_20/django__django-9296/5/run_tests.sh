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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 pagination.tests_llm.CustomPage.__init__ pagination.tests_llm.CustomPage.__iter__ pagination.tests_llm.CustomPage.__len__ pagination.tests_llm.CustomPaginator._get_page pagination.tests_llm.PaginatorIterationRegressionTests.test_iteration_after_page_getitem_does_not_share_state
coverage json -o coverage.json
: '>>>>> End Test Output'
