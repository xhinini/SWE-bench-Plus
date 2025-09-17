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
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 model_fields.tests_llm.FieldOrderingHashTests._make_field model_fields.tests_llm.FieldOrderingHashTests.test_exact_hash_matches_model_meta_tuple model_fields.tests_llm.FieldOrderingHashTests.test_hash_difference_with_and_without_model model_fields.tests_llm.FieldOrderingHashTests.test_hash_equality_for_fields_with_same_model model_fields.tests_llm.FieldOrderingHashTests.test_no_model_less_than_model_with_same_creation_counter model_fields.tests_llm.FieldOrderingHashTests.test_sorting_list_with_mixed_models_places_no_model_first
coverage json -o coverage.json
: '>>>>> End Test Output'
