#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 migrations.test_autodetector_llm.test_generate_renamed_models_with_dependency_from_hardcoded_fk migrations.test_autodetector_llm.test_only_relation_agnostic_fields_handles_missing_to_direct migrations.test_autodetector_llm.test_rename_field_with_hardcoded_fk_missing_to migrations.test_autodetector_llm.test_rename_model_old_hardcoded_new_normal_fk migrations.test_autodetector_llm.test_rename_model_old_normal_new_hardcoded_fk migrations.test_autodetector_llm.test_rename_model_with_hardcoded_fk_and_through_field migrations.test_autodetector_llm.test_rename_model_with_hardcoded_fk_missing_to migrations.test_autodetector_llm.test_rename_model_with_multiple_fks_some_missing_to
coverage json -o coverage.json
: '>>>>> End Test Output'
