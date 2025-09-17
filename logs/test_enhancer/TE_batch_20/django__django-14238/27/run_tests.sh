#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.test_autofield_llm.AutoFieldMetaRegressionTests.test_issubclass_with_mixed_tuple_first_arg model_fields.test_autofield_llm.AutoFieldMetaRegressionTests.test_issubclass_with_tuple_first_argument
coverage json -o coverage.json
: '>>>>> End Test Output'
