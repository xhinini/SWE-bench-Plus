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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 prefetch_related.test_models_llm.UUIDFieldPrepTests._db_value_for_uuid prefetch_related.test_models_llm.UUIDFieldPrepTests.setUp prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_db_prep_value_prepared_true_after_get_prep_value_dashed_string prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_db_prep_value_prepared_true_after_get_prep_value_hex_string prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_db_prep_value_prepared_true_after_get_prep_value_int prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_accepts_dashed_string prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_accepts_hex_string_without_dashes prefetch_related.test_models_llm.UUIDFieldPrepTests.test_get_prep_value_accepts_int
coverage json -o coverage.json
: '>>>>> End Test Output'
