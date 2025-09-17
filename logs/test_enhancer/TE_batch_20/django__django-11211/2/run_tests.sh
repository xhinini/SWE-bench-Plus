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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 prefetch_related.test_models_llm.UUIDFieldPrepTests.setUp prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_converts_hex_string_to_uuid prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_converts_int_to_uuid prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_empty_string_invalid_when_empty_strings_not_allowed prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_invalid_raises prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_with_lazy_hex_string prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_with_lazy_int
coverage json -o coverage.json
: '>>>>> End Test Output'
