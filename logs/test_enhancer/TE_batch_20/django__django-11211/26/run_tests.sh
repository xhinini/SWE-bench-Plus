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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 prefetch_related.test_models_llm.DummyConnection.__init__ prefetch_related.test_models_llm.DummyFeatures.__init__ prefetch_related.test_models_llm.UUIDFieldPrepTests.setUp prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_from_uuid_string_with_dashes_raises prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_with_32_char_hex_string prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_with_int prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_with_invalid_string_raises prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_with_uppercase_hex prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_zero_int
coverage json -o coverage.json
: '>>>>> End Test Output'
