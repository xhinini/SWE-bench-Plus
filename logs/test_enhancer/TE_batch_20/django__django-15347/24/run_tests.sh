#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 messages_tests.test_cookie_llm.MessageExtraTagsPreservationTests._roundtrip_with_encoder messages_tests.test_cookie_llm.MessageExtraTagsPreservationTests._roundtrip_with_serializer
coverage json -o coverage.json
: '>>>>> End Test Output'
