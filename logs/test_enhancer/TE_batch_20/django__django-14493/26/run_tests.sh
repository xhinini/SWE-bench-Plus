#!/bin/bash
set -uxo pipefail
source /opt/miniconda3/bin/activate
conda activate testbed
cd /testbed
export PYTHONIOENCODING=utf8
python --version
pip install -U coverage

: '>>>>> Start Test Output'
./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 staticfiles_tests.test_storage_llm.TestMaxPostProcessZero._save staticfiles_tests.test_storage_llm.TestMaxPostProcessZero.setUp staticfiles_tests.test_storage_llm.TestMaxPostProcessZero.tearDown staticfiles_tests.test_storage_llm.TestMaxPostProcessZero.test_fragment_handling_preserved_with_zero_passes staticfiles_tests.test_storage_llm.TestMaxPostProcessZero.test_keep_intermediate_files_true_behavior_with_zero_passes staticfiles_tests.test_storage_llm.TestMaxPostProcessZero.test_stored_name_no_infinite_loop_on_zero_passes staticfiles_tests.test_storage_llm.TestMaxPostProcessZero.test_stored_name_with_zero_passes_computes_hash_once staticfiles_tests.test_storage_llm.TestMaxPostProcessZero.test_url_converter_handles_relative_paths_with_zero_passes
coverage json -o coverage.json
: '>>>>> End Test Output'
