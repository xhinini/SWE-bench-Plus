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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 ordering.test_models_llm.FakeField.__init__ ordering.test_models_llm.FakeQuery.__init__ ordering.test_models_llm.FakeQuery.trim_joins ordering.test_models_llm.FindOrderingNameTests._assert_without_related_default ordering.test_models_llm.FindOrderingNameTests._make_setup_joins ordering.test_models_llm.FindOrderingNameTests.setUp ordering.test_models_llm.FindOrderingNameTests.test_prefixed_lookup_attname_equal_field ordering.test_models_llm.FindOrderingNameTests.test_prefixed_lookup_attname_equal_nested ordering.test_models_llm.FindOrderingNameTests.test_prefixed_lookup_attname_equal_owner ordering.test_models_llm.FindOrderingNameTests.test_prefixed_lookup_attname_equal_root ordering.test_models_llm.FindOrderingNameTests.test_prefixed_lookup_attname_equal_y
coverage json -o coverage.json
: '>>>>> End Test Output'
